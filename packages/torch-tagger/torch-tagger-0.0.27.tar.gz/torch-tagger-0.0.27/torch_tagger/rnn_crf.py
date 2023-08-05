# -*- coding: utf-8 -*-
"""
.. module:: rnn_crf

Based https://pytorch.org/tutorials/beginner/nlp/advanced_tutorial.html

Modified by InfinityFuture

"""

import numpy as np
import torch
from torch import nn
from sklearn.preprocessing import normalize

from torch_tagger.utils import START_TAG, STOP_TAG, DEVICE, sequence_mask

class RNNCRF(nn.Module): # pylint: disable=too-many-instance-attributes
    """
    RNN + CRF
    """

    def __init__(self, # pylint: disable=too-many-arguments
                 vocab_size,
                 tag_to_ix,
                 embedding_dim,
                 hidden_dim,
                 num_layers=1,
                 bidirectional=True,
                 embedding_dropout_p=0.0,
                 rnn_dropout_p=0.0,
                 rnn_type='lstm',
                 device=DEVICE,
                 embedding_trainable=True):
        """
        Embedding Random Init:

        [He et al.2015] Kaiming He, Xiangyu Zhang, Shaoqing
        Ren, and Jian Sun. 2015. Delving deep into recti-
        fiers: Surpassing human-level performance on ima-
        genet classification. In Proceedings of the IEEE In-
        ternational Conference on Computer Vision, pages
        1026–1034.
        """
        super(RNNCRF, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size
        self.tag_to_ix = tag_to_ix
        self.tagset_size = len(tag_to_ix)
        self.num_layers = num_layers
        self.bidirectional = bidirectional
        self.embedding_dropout_p = embedding_dropout_p
        self.rnn_dropout_p = rnn_dropout_p
        self.device = device
        self.rnn_type = rnn_type
        self.embedding_trainable = embedding_trainable

        # hidden state of RNN
        self.hidden = None
        # Embedding Layer
        self.word_embeds = nn.Embedding(vocab_size, embedding_dim)
        self.init_embedding()
        # RNN Layer
        if rnn_type == 'lstm':
            self.rnn = nn.LSTM(
                embedding_dim,
                hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional
            )
        elif rnn_type == 'gru':
            self.rnn = nn.GRU(
                embedding_dim,
                hidden_dim,
                num_layers=num_layers,
                bidirectional=bidirectional
            )
        else:
            raise Exception('Invalid rnn_type')
        init_rnn_weight(self.rnn, self.rnn_type)

        self.embedding_dropout = nn.Dropout(self.embedding_dropout_p)
        self.rnn_dropout = nn.Dropout(self.rnn_dropout_p)

        # Maps the output of the LSTM into tag space.
        # Output Projection Layer
        self.hidden2tag = nn.Linear(
            hidden_dim * 2 if bidirectional else hidden_dim,
            self.tagset_size
        )
        init_linear_weight(self.hidden2tag)

        # Matrix of transition parameters.  Entry i,j is the score of
        # transitioning *to* i *from* j.
        self.transitions = nn.Parameter(
            torch.randn(self.tagset_size, self.tagset_size))

        # These two statements enforce the constraint that we never transfer
        # to the start tag and we never transfer from the stop tag
        self.transitions.data[tag_to_ix[START_TAG], :] = -10000
        self.transitions.data[:, tag_to_ix[STOP_TAG]] = -10000

    def init_embedding(self, pretrained_embedding=None):
        """Init embedding variable"""
        if pretrained_embedding is not None:
            assert len(pretrained_embedding.shape) == 2
            assert pretrained_embedding.shape[0] == self.vocab_size
            assert pretrained_embedding.shape[1] == self.embedding_dim
            pretrained_embedding = normalize(pretrained_embedding)
            print('loaded pre-trained vectors', pretrained_embedding.shape)
            self.word_embeds.load_state_dict({
                'weight': torch.from_numpy(pretrained_embedding)
            })
        else:
            init_embedding = np.random.uniform(
                -np.sqrt(3. / self.embedding_dim),
                np.sqrt(3. / self.embedding_dim),
                size=(self.vocab_size, self.embedding_dim)
            )
            self.word_embeds.load_state_dict({
                'weight': torch.from_numpy(init_embedding)
            })
        self.word_embeds.weight.requires_grad = self.embedding_trainable


    def init_hidden(self, batch_size):
        """Initilize the hidden for RNN"""
        bidirectional = self.bidirectional
        hidden_dim = self.hidden_dim
        num_layers = self.num_layers
        rnn_type = self.rnn_type
        if rnn_type == 'lstm':
            return (
                torch.zeros(
                    2 * num_layers if bidirectional else num_layers,
                    batch_size,
                    hidden_dim
                ).to(self.device),
                torch.zeros(
                    2 * num_layers if bidirectional else num_layers,
                    batch_size,
                    hidden_dim
                ).to(self.device),
            )
        if rnn_type == 'gru':
            return torch.zeros(
                2 * num_layers if bidirectional else num_layers,
                batch_size,
                hidden_dim
            ).to(self.device)
        raise Exception('Unknown rnn_type')

    def _forward_alg(self, feats_batch, lengths_batch): # pylint: disable=too-many-locals
        """Get CRF result"""
        # feats_batch dim: [batch_size, seq_len, target_dim]
        # lengths_batch dim: [batch_size]
        batch_size = feats_batch.size()[0]
        alpha_batch = []
        # Do the forward algorithm to compute the partition function
        init_alphas = torch.full((batch_size, self.tagset_size), -10000.).to(self.device)
        # START_TAG has all of the score.
        init_alphas[:, self.tag_to_ix[START_TAG]] = 0.

        for i in range(batch_size):
            feats = feats_batch[i]
            length = lengths_batch[i]

            # Wrap in a variable so that we will get automatic backprop
            forward_var = init_alphas[i]

            # Iterate through the sentence
            for feat in feats[:length]:
                alphas_t = []  # The forward tensors at this timestep
                for next_tag in range(self.tagset_size):
                    # broadcast the emission score: it is the same regardless of
                    # the previous tag
                    emit_score = feat[next_tag].view(
                        1, -1).expand(1, self.tagset_size)
                    # the ith entry of trans_score is the score of transitioning to
                    # next_tag from i
                    trans_score = self.transitions[next_tag].view(1, -1)
                    # The ith entry of next_tag_var is the value for the
                    # edge (i -> next_tag) before we do log-sum-exp
                    next_tag_var = forward_var
                    next_tag_var = next_tag_var + trans_score
                    next_tag_var = next_tag_var + emit_score
                    # The forward variable for this tag is log-sum-exp of all the
                    # scores.
                    alphas_t.append(log_sum_exp(next_tag_var).view(1))
                forward_var = torch.cat(alphas_t).view(1, -1)
            terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_TAG]]
            alpha = terminal_var
            alpha = log_sum_exp(alpha)
            alpha /= length.float()
            alpha_batch.append(alpha)
        return torch.stack(alpha_batch)

    def _forward_alg_batch(self, feats, lengths, masks): # pylint: disable=too-many-locals
        """Get CRF result, batch version"""
        # feats dim: [batch_size, seq_len, target_dim]
        # lengths dim: [batch_size]
        # masks dim: [batch_size, seq_len]
        batch_size = feats.size()[0]
        # Do the forward algorithm to compute the partition function
        # init_alphas dim: [batch_size, tagset_size]
        init_alphas = torch.full((batch_size, self.tagset_size), -10000.).to(self.device)
        # START_TAG has all of the score.
        init_alphas[:, self.tag_to_ix[START_TAG]] = 0.

        # Wrap in a variable so that we will get automatic backprop
        forward_var = init_alphas

        # feats dim: [seq_len, batch_size, target_dim]
        feats = feats.permute(1, 0, 2)
        # Iterate through the sentence
        forward_var_batch = []
        for i, feat in enumerate(feats):
            alphas_t = []  # The forward tensors at this timestep
            for next_tag in range(self.tagset_size):
                # broadcast the emission score: it is the same regardless of
                # the previous tag
                emit_score = feat[:, next_tag].view(
                    batch_size, 1).expand(batch_size, self.tagset_size)
                # the ith entry of trans_score is the score of transitioning to
                # next_tag from i
                trans_score = self.transitions[next_tag].view(1, -1).expand(
                    batch_size, self.tagset_size)
                # The ith entry of trans_score is the value for the
                # edge (i -> next_tag) before we do log-sum-exp
                mask = masks[:, i].contiguous().view(batch_size, 1)
                trans_score = trans_score * mask
                emit_score = emit_score * mask
                next_tag_var = forward_var
                next_tag_var = next_tag_var + trans_score
                next_tag_var = next_tag_var + emit_score
                # The forward variable for this tag is log-sum-exp of all the
                # scores.
                log_vec = log_sum_exp_batch(next_tag_var).view(1, -1)
                raw_vec = forward_var[:, 0].view(1, -1)
                vec_beforce_choice = torch.cat([raw_vec, log_vec])
                vec_beforce_choice = vec_beforce_choice.permute(1, 0)
                tmp = vec_beforce_choice.gather(1, mask.long()).squeeze()

                alphas_t.append(tmp)

            forward_var = torch.stack(alphas_t)
            forward_var = forward_var.permute(1, 0)
            forward_var_batch.append(forward_var)

        forward_var = torch.stack([
            forward_var_batch[l - 1][i]
            for i, l in enumerate(lengths)
        ])

        terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_TAG]]
        alpha = terminal_var
        alpha = log_sum_exp_batch(alpha)
        alpha = alpha / lengths.float()
        return alpha

    def _get_rnn_features(self, sentence, is_train=True):
        """Get the output of RNN model"""
        # sentence dim: [batch_size, seq_len]
        batch_size, _ = sentence.size()

        self.hidden = self.init_hidden(batch_size)

        # embeds dim: [batch_size, seq_len, embedding_size]
        embeds = self.word_embeds(sentence)
        if is_train:
            embeds = self.embedding_dropout(embeds)
        # embeds dim: [seq_len, batch_size, embedding_size]
        # embeds = embeds.view(seq_len, batch_size, -1)
        embeds = embeds.permute(1, 0, 2)

        # rnn_out dim: [seq_len, batch_size, hidden_dim]
        rnn_out, self.hidden = self.rnn(embeds, self.hidden)
        # When your batch_size > 1, you should use permute not view
        # rnn_out = rnn_out.view(batch_size, seq_len, self.hidden_dim)
        rnn_out = rnn_out.permute(1, 0, 2)
        # rnn_feats dim: [batch_size, seq_len, target_dim]
        rnn_feats = self.hidden2tag(rnn_out)

        return rnn_feats

    def _score_sentence(self, feats_batch, tags_batch, lengths_batch):
        """Get the gold standard of sentences"""
        # Gives the score of a provided tag sequence
        # feats_batch dim: [batch_size, seq_len, target_dim]
        # tags_batch dim: [batch_size, seq_len]
        # lengths_batch dim: [batch_size]
        batch_size = feats_batch.size()[0]
        score_batch = []
        for i in range(batch_size):
            score = torch.zeros(1).to(self.device)
            feats = feats_batch[i]
            tags = tags_batch[i]
            length = lengths_batch[i]

            tags = torch.cat([
                torch.tensor([ # pylint: disable=not-callable
                    self.tag_to_ix[START_TAG]
                ], dtype=torch.long).to(self.device),
                tags[:length]
            ])

            for j, feat in enumerate(feats[:length]):
                score = score + \
                    self.transitions[tags[j + 1], tags[j]] + feat[tags[j + 1]]
            score = score + self.transitions[self.tag_to_ix[STOP_TAG], tags[-1]]
            score = score / length.float()
            score_batch.append(score)
        return torch.cat(score_batch)

    def _score_sentence_batch(self, feats, tags, lengths, masks): # pylint: disable=too-many-locals
        """Get the gold standard of sentences, batch version"""
        # Gives the score of a provided tag sequence
        # feats dim: [batch_size, seq_len, target_dim]
        # tags dim: [batch_size, seq_len]
        # lengths dim: [batch_size]
        # masks dim: [batch_size, seq_len]
        batch_size = feats.size()[0]

        score = torch.zeros(batch_size).to(self.device)

        start = torch.tensor([ # pylint: disable=not-callable
            self.tag_to_ix[START_TAG]
        ], dtype=torch.long).expand(batch_size, 1).to(self.device)

        tags = torch.cat([
            start,
            tags
        ], dim=1)

        feats = feats.permute(1, 0, 2)
        for j, feat in enumerate(feats):
            mask = masks[:, j].contiguous().view(batch_size, 1)
            tag_next, tag_cur = tags[:, j + 1], tags[:, j]
            score = score \
                + self.transitions[tag_next, tag_cur] * mask \
                + feat[:, tag_next] * mask

        # score = score + self.transitions[self.tag_to_ix[STOP_TAG], tags[:, -1]]
        for i, (tag, length) in enumerate(zip(tags, lengths)):
            score[i] = score[i] + self.transitions[self.tag_to_ix[STOP_TAG]][tag[length]]
        score = score / lengths.float()

        return score.diag()

    def _viterbi_decode(self, feats_batch): # pylint: disable=too-many-locals
        """Inference result"""
        # feats_batch dim: [batch_size, seq_len, target_dim]
        batch_size = feats_batch.size()[0]
        path_scores, best_paths = [], []
        for i in range(batch_size):
            feats = feats_batch[i]
            backpointers = []

            # Initialize the viterbi variables in log space
            # init_vvars dim: [1, tagset_size]
            init_vvars = torch.full((1, self.tagset_size), -10000.).to(self.device)
            init_vvars[0][self.tag_to_ix[START_TAG]] = 0

            # forward_var at step i holds the viterbi variables for step i-1
            forward_var = init_vvars
            for feat in feats:
                bptrs_t = []  # holds the backpointers for this step
                viterbivars_t = []  # holds the viterbi variables for this step

                for next_tag in range(self.tagset_size):
                    # next_tag_var[i] holds the viterbi variable for tag i at the
                    # previous step, plus the score of transitioning
                    # from tag i to next_tag.
                    # We don't include the emission scores here because the max
                    # does not depend on them (we add them in below)
                    # next_tag_var dim: [1, tagset_size]
                    next_tag_var = forward_var + self.transitions[next_tag]
                    best_tag_id = argmax(next_tag_var)
                    bptrs_t.append(best_tag_id)
                    viterbivars_t.append(next_tag_var[0][best_tag_id].view(1))
                # Now add in the emission scores, and assign forward_var to the set
                # of viterbi variables we just computed
                # forward_var dim: [1, tagset_size]
                forward_var = (torch.cat(viterbivars_t) + feat).view(1, -1)
                backpointers.append(bptrs_t)

            # Transition to STOP_TAG
            # terminal_var dim: [1, tagset_size]
            terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_TAG]]
            best_tag_id = argmax(terminal_var)
            path_score = terminal_var[0][best_tag_id]

            # Follow the back pointers to decode the best path.
            best_path = [best_tag_id]
            for bptrs_t in reversed(backpointers):
                best_tag_id = bptrs_t[best_tag_id]
                best_path.append(best_tag_id)
            # Pop off the start tag (we dont want to return that to the caller)
            start = best_path.pop()
            assert start == self.tag_to_ix[START_TAG]  # Sanity check
            best_path.reverse()

            path_scores.append(path_score)
            best_paths.append(best_path)

        path_scores = torch.stack(path_scores)
        best_paths = np.array(best_paths)

        return path_scores, best_paths

    def _viterbi_decode_batch(self, feats): # pylint: disable=too-many-locals
        """Inference result"""
        # feats dim: [batch_size, seq_len, target_dim]
        batch_size = feats.size()[0]

        backpointers = []

        # Initialize the viterbi variables in log space
        # init_vvars dim: [batch_size, tagset_size]
        init_vvars = torch.full((batch_size, self.tagset_size), -10000.).to(self.device)
        init_vvars[:, self.tag_to_ix[START_TAG]] = 0

        # forward_var at step i holds the viterbi variables for step i-1
        forward_var = init_vvars

        # feats dim: [seq_len, batch_size, target_dim]
        feats = feats.permute(1, 0, 2)
        # feat dim: [batch_size, target_dim]
        for feat in feats:
            bptrs_t = []  # holds the backpointers for this step
            viterbivars_t = []  # holds the viterbi variables for this step

            for next_tag in range(self.tagset_size):
                # next_tag_var[i] holds the viterbi variable for tag i at the
                # previous step, plus the score of transitioning
                # from tag i to next_tag.
                # We don't include the emission scores here because the max
                # does not depend on them (we add them in below)
                # next_tag_var dim: [batch_size, tagset_size]
                next_tag_var = forward_var + self.transitions[
                    next_tag
                ].view(1, -1).expand(batch_size, self.tagset_size)
                best_tag_id = argmax_batch(next_tag_var)
                bptrs_t.append(best_tag_id.view(1, -1))
                tmp = next_tag_var.gather(1, best_tag_id.view(-1, 1)).squeeze()
                viterbivars_t.append(tmp.view(1, batch_size))
            # Now add in the emission scores, and assign forward_var to the set
            # of viterbi variables we just computed
            # forward_var dim: [batch_size, tagset_size]
            tmp = torch.cat(viterbivars_t)
            tmp = tmp.permute(1, 0)
            forward_var = (tmp + feat).view(batch_size, -1)
            backpointers.append(torch.cat(bptrs_t))

        # Transition to STOP_TAG
        # terminal_var dim: [1, tagset_size]
        terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_TAG]]
        best_tag_id = argmax_batch(terminal_var)
        path_score = [terminal_var[i][x] for i, x in enumerate(best_tag_id)]

        # Follow the back pointers to decode the best path.
        # backpointers dim: [seq_len, tagset_size, batch_size]
        backpointers = torch.stack(backpointers)
        # backpointers dim: [seq_len, batch_size, tagset_size]
        backpointers = backpointers.permute(0, 2, 1)
        best_path = [best_tag_id]
        for bptrs_t in reversed(backpointers):
            if batch_size > 1:
                best_tag_id = bptrs_t.gather(1, best_tag_id.view(-1, 1)).squeeze()
                best_path.append(best_tag_id)
            else:
                best_tag_id = bptrs_t[0][best_tag_id]
                best_path.append(best_tag_id)
        # Pop off the start tag (we dont want to return that to the caller)
        start = best_path.pop()
        assert np.sum(
            start.cpu().detach().numpy() - np.array([
                self.tag_to_ix[START_TAG]
            ] * batch_size)
        ) <= 1e-5
        best_path.reverse()

        path_score = torch.stack(path_score)
        best_path = torch.stack(best_path)
        best_path = best_path.permute(1, 0).cpu().detach().numpy()

        return path_score, best_path

    def neg_log_likelihood(self, sentence, tags, lengths):
        """Calculate loss"""
        rnn_feats = self._get_rnn_features(sentence)
        rnn_feats = self.rnn_dropout(rnn_feats)

        seq_len = rnn_feats.size()[1]
        masks = sequence_mask(lengths, seq_len)

        forward_score = self._forward_alg_batch(rnn_feats, lengths, masks)
        gold_score = self._score_sentence_batch(rnn_feats, tags, lengths, masks)

        # forward_score_slow = self._forward_alg(rnn_feats, lengths)
        # gold_score_slow = self._score_sentence(rnn_feats, tags, lengths)
        # print(torch.sum(forward_score_slow - forward_score))
        # print(torch.sum(gold_score_slow - gold_score))

        loss = torch.mean(forward_score - gold_score)
        return loss

    def forward(self, sentence): # pylint: disable=arguments-differ
        """Main forward function, predict only"""
        # Get the emission scores from the BiLSTM
        rnn_feats = self._get_rnn_features(sentence, is_train=False)
        # Find the best path, given the features.
        # score, tag_seq = self._viterbi_decode(rnn_feats)
        score, tag_seq = self._viterbi_decode_batch(rnn_feats)
        return score, tag_seq

def argmax(vec) -> int:
    """return the argmax as a python int"""
    _, idx = torch.max(vec, 1)
    return idx.item()

def log_sum_exp(vec):
    """Compute log sum exp in a numerically stable way for the forward algorithm
    vec dim: [n]
    """
    max_score = vec[0, argmax(vec)]
    max_score_broadcast = max_score.view(1, -1).expand(1, vec.size()[1])
    tmp = vec - max_score_broadcast
    tmp = torch.exp(tmp)
    tmp = torch.sum(tmp)
    tmp = torch.log(tmp)
    tmp = max_score + tmp
    return tmp

def argmax_batch(vec) -> torch.Tensor:
    """Batch version of argmax"""
    _, idx = torch.max(vec, 1)
    return idx

def log_sum_exp_batch(vec):
    """Batch version of log_sum_exp
    vec dim: [batch_size, n]
    """
    batch_size = vec.size()[0]
    amax = argmax_batch(vec)
    max_score = vec.gather(1, amax.view(-1, 1))
    max_score = max_score.view(1, -1)
    max_score_broadcast = max_score.view(batch_size, -1)
    max_score_broadcast = max_score_broadcast.expand(batch_size, vec.size()[1])
    tmp = vec - max_score_broadcast
    tmp = torch.exp(tmp)
    tmp = torch.sum(tmp, -1)
    tmp = torch.log(tmp)
    tmp = max_score + tmp
    return tmp[0]

def get_weight(dim0, dim1):
    """Weight random parameter:

    [Glorot and Bengio2010] Xavier Glorot and Yoshua
    Bengio. 2010. Understanding the difficulty of
    training deep feedforward neural networks. In In-
    ternational conference on artificial intelligence and
    statistics, pages 249–256.
    """
    weight_init = np.random.uniform(
        -np.sqrt(6. / (dim0 + dim1)),
        np.sqrt(6. / (dim0 + dim1)),
        size=(dim0, dim1)
    )
    return torch.from_numpy(weight_init)

def get_bias(dim):
    """Init bias"""
    bias_init = np.zeros(dim)
    return torch.from_numpy(bias_init)

def get_lstm_bias(dim):
    """Init bias for LSTM

    (b_ii|b_if|b_ig|b_io), of shape (4*hidden_size)

    set f-gate is ones, zeros for others
    """
    assert dim % 4 == 0
    hdim = dim // 4
    bias_init = np.concatenate([
        np.zeros(hdim),
        np.ones(hdim), # Set forget gate bias to 1
        np.zeros(hdim),
        np.zeros(hdim),
    ])
    return torch.from_numpy(bias_init)

def init_linear_weight(layer):
    """init weight for nn.Linear"""
    weight_dim0, weight_dim1 = layer.weight.size()
    bias_dim = layer.bias.size()[0]
    layer.load_state_dict({
        'weight': get_weight(weight_dim0, weight_dim1),
        'bias': get_bias(bias_dim),
    })

def init_rnn_weight(layer, rnn_type):
    """init weight for nn.LSTM and nn.GRU"""
    state_dict = {}
    for weight_name in dir(layer):
        if weight_name.startswith('weight_') or weight_name.startswith('bias_'):
            if weight_name.startswith('weight'):
                weight_dim0, weight_dim1 = getattr(layer, weight_name).size()
                weight = get_weight(weight_dim0, weight_dim1)
                state_dict[weight_name] = weight
            if weight_name.startswith('bias'):
                bias_dim = getattr(layer, weight_name).size()[0]
                if rnn_type == 'lstm':
                    bias = get_lstm_bias(bias_dim)
                else:
                    bias = get_bias(bias_dim)
                state_dict[weight_name] = bias
    layer.load_state_dict(state_dict)
