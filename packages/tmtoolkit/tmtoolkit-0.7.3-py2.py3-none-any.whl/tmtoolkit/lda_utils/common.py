# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
from collections import OrderedDict, defaultdict
import itertools
import logging
import multiprocessing as mp
import atexit
import ctypes

import six
import numpy as np
import pandas as pd
from scipy.sparse.coo import coo_matrix
from scipy.sparse import issparse


from ..utils import pickle_data, unpickle_file


logger = logging.getLogger('tmtoolkit')


DEFAULT_TOPIC_NAME_FMT = 'topic_{i1}'
DEFAULT_RANK_NAME_FMT = 'rank_{i1}'


def top_n_from_distribution(distrib, top_n=10, row_labels=None, col_labels=None, val_labels=None):
    """
    Get `top_n` values from LDA model's distribution `distrib` as DataFrame. Can be used for topic-word distributions
    and document-topic distributions. Set `row_labels` to a format string or a list. Set `col_labels` to a format
    string for the column names. Set `val_labels` to return value labels instead of pure values (probabilities).
    """
    if len(distrib) == 0:
        raise ValueError('`distrib` must contain values')

    if top_n < 1:
        raise ValueError('`top_n` must be at least 1')
    elif top_n > distrib.shape[1]:
        raise ValueError('`top_n` cannot be larger than num. of values in `distrib` rows')

    if row_labels is None:
        row_label_fixed = None
    elif isinstance(row_labels, six.string_types):
        row_label_fixed = row_labels
    else:
        row_label_fixed = None

    if val_labels is not None and type(val_labels) in (list, tuple):
        val_labels = np.array(val_labels)

    if col_labels is None:
        columns = range(top_n)
    else:
        columns = [col_labels.format(i0=i, i1=i+1) for i in range(top_n)]

    series = []

    for i, row_distrib in enumerate(distrib):
        if row_label_fixed:
            row_name = row_label_fixed.format(i0=i, i1=i+1)
        else:
            if row_labels is not None:
                row_name = row_labels[i]
            else:
                row_name = None

        # `sorter_arr` is an array of indices that would sort another array by `row_distrib` (from low to high!)
        sorter_arr = np.argsort(row_distrib)

        if val_labels is None:
            sorted_vals = row_distrib[sorter_arr][:-(top_n + 1):-1]
        else:
            if isinstance(val_labels, six.string_types):
                sorted_vals = [val_labels.format(i0=i, i1=i+1, val=row_distrib[i]) for i in sorter_arr[::-1]][:top_n]
            else:
                # first brackets: sort vocab by `sorter_arr`
                # second brackets: slice operation that reverts ordering (:-1) and then selects only `n_top` number of
                # elements
                sorted_vals = val_labels[sorter_arr][:-(top_n + 1):-1]

        series_kwargs = dict(index=columns)
        if row_name is not None:
            series_kwargs['name'] = row_name

        series.append(pd.Series(sorted_vals, **series_kwargs))

    return pd.DataFrame(series)


def top_words_for_topics(topic_word_distrib, top_n, vocab=None):
    if not isinstance(topic_word_distrib, np.ndarray) or topic_word_distrib.ndim != 2:
        raise ValueError('`topic_word_distrib` must be a 2D NumPy array')

    if len(topic_word_distrib) == 0:
        raise ValueError('`topic_word_distrib` cannot be empty')

    if vocab is not None:
        if not isinstance(vocab, np.ndarray) or vocab.ndim != 1:
            raise ValueError('`vocab` must be a 1D NumPy array')

        if len(vocab) == 0:
            raise ValueError('`vocab` cannot be empty')

        if topic_word_distrib.shape[1] != len(vocab):
            raise ValueError('shapes of provided `topic_word_distrib` and `vocab` do not match (vocab sizes differ)')

    if top_n < 1:
        raise ValueError('`top_n` must be at least 1')
    elif top_n > topic_word_distrib.shape[1]:
        raise ValueError('`top_n` cannot be larger than vocab size')

    topic_words = []

    for topic in topic_word_distrib:
        sorter_arr = np.argsort(topic)
        if vocab is None:
            topic_words.append(sorter_arr[:-(top_n+1):-1])
        else:
            topic_words.append(vocab[sorter_arr][:-(top_n+1):-1])

    return topic_words


def _join_value_and_label_dfs(vals, labels, top_n, val_fmt=None, row_labels=None, col_labels=None, index_name=None):
    val_fmt = val_fmt or '{lbl} ({val:.4})'
    col_labels = col_labels or DEFAULT_RANK_NAME_FMT
    index_name = index_name or 'document'

    if col_labels is None:
        columns = range(top_n)
    else:
        columns = [col_labels.format(i0=i, i1=i+1) for i in range(top_n)]

    df = pd.DataFrame(columns=columns)

    for i, (_, row) in enumerate(labels.iterrows()):
        joined = []
        for j, lbl in enumerate(row):
            val = vals.iloc[i, j]
            joined.append(val_fmt.format(lbl=lbl, val=val))

        if row_labels is not None:
            if isinstance(row_labels, six.string_types):
                row_name = row_labels.format(i0=i, i1=i+1)
            else:
                row_name = row_labels[i]
        else:
            row_name = None

        row_data = pd.Series(joined, name=row_name, index=columns)
        df = df.append(row_data)

    df.index.name = index_name

    return df


def ldamodel_top_topic_words(topic_word_distrib, vocab, top_n=10, val_fmt=None, col_labels=None, index_name=None):
    df_values = top_n_from_distribution(topic_word_distrib, top_n=top_n,
                                        row_labels=DEFAULT_TOPIC_NAME_FMT, val_labels=None)
    df_labels = top_n_from_distribution(topic_word_distrib, top_n=top_n,
                                        row_labels=DEFAULT_TOPIC_NAME_FMT, val_labels=vocab)
    return _join_value_and_label_dfs(df_values, df_labels, top_n, row_labels=DEFAULT_TOPIC_NAME_FMT,
                                     val_fmt=val_fmt, col_labels=col_labels, index_name=index_name)


def ldamodel_top_doc_topics(doc_topic_distrib, doc_labels, top_n=3, val_fmt=None, col_labels=None, index_name=None):
    df_values = top_n_from_distribution(doc_topic_distrib, top_n=top_n,
                                        row_labels=doc_labels, val_labels=None)
    df_labels = top_n_from_distribution(doc_topic_distrib, top_n=top_n,
                                        row_labels=doc_labels, val_labels=DEFAULT_TOPIC_NAME_FMT)
    return _join_value_and_label_dfs(df_values, df_labels, top_n, row_labels=doc_labels,
                                     val_fmt=val_fmt, col_labels=col_labels, index_name=index_name)


def ldamodel_full_topic_words(topic_word_distrib, vocab, fmt_rownames=DEFAULT_TOPIC_NAME_FMT):
    if fmt_rownames:
        rownames = [fmt_rownames.format(i0=i, i1=i+1) for i in range(topic_word_distrib.shape[0])]
    else:
        rownames = None

    return pd.DataFrame(topic_word_distrib, columns=vocab, index=rownames)


def ldamodel_full_doc_topics(doc_topic_distrib, doc_labels, fmt_colnames=DEFAULT_TOPIC_NAME_FMT):
    if fmt_colnames:
        colnames = [fmt_colnames.format(i0=i, i1=i+1) for i in range(doc_topic_distrib.shape[1])]
    else:
        colnames = None

    return pd.DataFrame(doc_topic_distrib, columns=colnames, index=doc_labels)


def print_ldamodel_distribution(distrib, row_labels, val_labels, top_n=10):
    """
    Print `n_top` top values from a LDA model's distribution `distrib`. Can be used for topic-word distributions and
    document-topic distributions.
    """

    df_values = top_n_from_distribution(distrib, top_n=top_n, row_labels=row_labels, val_labels=None)
    df_labels = top_n_from_distribution(distrib, top_n=top_n, row_labels=row_labels, val_labels=val_labels)

    for i, (ind, row) in enumerate(df_labels.iterrows()):
        print(ind)
        for j, label in enumerate(row):
            val = df_values.iloc[i, j]
            print('> #%d. %s (%f)' % (j + 1, label, val))


def print_ldamodel_topic_words(topic_word_distrib, vocab, n_top=10):
    """Print `n_top` values from a LDA model's topic-word distributions."""
    print_ldamodel_distribution(topic_word_distrib, row_labels=DEFAULT_TOPIC_NAME_FMT, val_labels=vocab,
                                top_n=n_top)


def print_ldamodel_doc_topics(doc_topic_distrib, doc_labels, n_top=3):
    """Print `n_top` values from a LDA model's document-topic distributions."""
    print_ldamodel_distribution(doc_topic_distrib, row_labels=doc_labels, val_labels=DEFAULT_TOPIC_NAME_FMT,
                                top_n=n_top)


def save_ldamodel_summary_to_excel(excel_file, topic_word_distrib, doc_topic_distrib, doc_labels, vocab,
                                   top_n_topics=10, top_n_words=10, dtm=None,
                                   rank_label_fmt=None, topic_label_fmt=None):
    rank_label_fmt = rank_label_fmt or DEFAULT_RANK_NAME_FMT
    topic_label_fmt = topic_label_fmt or DEFAULT_TOPIC_NAME_FMT
    excel_writer = pd.ExcelWriter(excel_file)
    sheets = OrderedDict()

    # doc-topic distribution sheets
    sheets['top_doc_topics_vals'] = top_n_from_distribution(doc_topic_distrib, top_n=top_n_topics,
                                                            row_labels=doc_labels,
                                                            col_labels=rank_label_fmt)
    sheets['top_doc_topics_labels'] = top_n_from_distribution(doc_topic_distrib, top_n=top_n_topics,
                                                              row_labels=doc_labels,
                                                              col_labels=rank_label_fmt,
                                                              val_labels=topic_label_fmt)
    sheets['top_doc_topics_labelled_vals'] = ldamodel_top_doc_topics(doc_topic_distrib, doc_labels, top_n=top_n_topics)

    # topic-word distribution sheets
    sheets['top_topic_word_vals'] = top_n_from_distribution(topic_word_distrib, top_n=top_n_words,
                                                            row_labels=topic_label_fmt,
                                                            col_labels=rank_label_fmt)
    sheets['top_topic_word_labels'] = top_n_from_distribution(topic_word_distrib, top_n=top_n_words,
                                                              row_labels=topic_label_fmt,
                                                              col_labels=rank_label_fmt,
                                                              val_labels=vocab)
    sheets['top_topic_words_labelled_vals'] = ldamodel_top_topic_words(topic_word_distrib, vocab, top_n=top_n_words)

    if dtm is not None:
        doc_lengths = get_doc_lengths(dtm)
        marg_topic_distr = get_marginal_topic_distrib(doc_topic_distrib, doc_lengths)
        row_names = [DEFAULT_TOPIC_NAME_FMT.format(i0=i, i1=i + 1) for i in range(len(marg_topic_distr))]
        sheets['marginal_topic_distrib'] = pd.DataFrame(marg_topic_distr, columns=['marginal_topic_distrib'],
                                                        index=row_names)

    for sh_name, sh_data in sheets.items():
        sh_data.to_excel(excel_writer, sh_name)

    excel_writer.save()

    return sheets


def save_ldamodel_to_pickle(picklefile, model, vocab, doc_labels, dtm=None, **kwargs):
    """Save a LDA model as pickle file."""
    pickle_data({'model': model, 'vocab': vocab, 'doc_labels': doc_labels, 'dtm': dtm}, picklefile)


def load_ldamodel_from_pickle(picklefile, **kwargs):
    """Load a LDA model from a pickle file."""
    return unpickle_file(picklefile, **kwargs)


def dtm_to_gensim_corpus(dtm):
    import gensim

    # DTM with documents to words sparse matrix in COO format has to be converted to transposed sparse matrix in CSC
    # format
    dtm_t = dtm.transpose()

    if issparse(dtm_t):
        if dtm_t.format != 'csc':
            dtm_sparse = dtm_t.tocsc()
        else:
            dtm_sparse = dtm_t
    else:
        from scipy.sparse.csc import csc_matrix
        dtm_sparse = csc_matrix(dtm_t)

    return gensim.matutils.Sparse2Corpus(dtm_sparse)


def dtm_and_vocab_to_gensim_corpus_and_dict(dtm, vocab, as_gensim_dictionary=True):
    corpus = dtm_to_gensim_corpus(dtm)

    # vocabulary array has to be converted to dict with index -> word mapping
    id2word = dict(zip(range(len(vocab)), vocab))

    if as_gensim_dictionary:
        import gensim
        return corpus, gensim.corpora.dictionary.Dictionary().from_corpus(corpus, id2word)
    else:
        return corpus, id2word


class FakedGensimDict(object):
    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError('`data` must be an instance of `dict`')

        self.id2token = data
        self.token2id = {v: k for k, v in data.items()}

    @staticmethod
    def from_vocab(vocab):
        return FakedGensimDict(dict(zip(range(len(vocab)), vocab)))


def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)


def results_by_parameter(res, param, sort_by=None, sort_desc=False,
                         crossvalid_use_measurment='validation',
                         crossvalid_reduce=False,
                         crossvalid_reduce_fn=None):
    """
    Takes a list of evaluation results `res` returned by a LDA evaluation function (a list in the form
    `[(parameter_set_1, {'<metric_name>': result_1, ...}), ..., (parameter_set_n, {'<metric_name>': result_n, ...})]`)
    and returns a list with tuple pairs using  only the parameter `param` from the parameter sets in the evaluation
    results such that the returned list is
    `[(param_1, {'<metric_name>': result_1, ...}), ..., (param_n, {'<metric_name>': result_n, ...})]`.
    Optionally order either by parameter value (`sort_by=None` - the default) or by result metric
    (`sort_by='<metric name>'`).
    """
    if len(res) == 0:
        return []

    if crossvalid_use_measurment not in ('validation', 'training'):
        raise ValueError('`crossvalid_use_measurment` must be either "validation" or "training" to use the validation '
                         'or training measurements.')

    tuples = [(p[param], r) for p, r in res]

    if type(tuples[0][1]) in (list, tuple):  # cross validation results
        if len(tuples[0][1]) < 1 or len(tuples[0][1][0]) != 2:
            raise ValueError('invalid evaluation results from cross validation passed')

        mean = lambda x: sum(x) / len(x)
        crossvalid_reduce_fn = crossvalid_reduce_fn or mean

        use_measurements_idx = 0 if crossvalid_use_measurment == 'training' else 1
        measurements = [(p, [pair[use_measurements_idx] for pair in r]) for p, r in tuples]
        measurements_reduced = [(p, crossvalid_reduce_fn(r)) for p, r in measurements]

        sort_by_idx = 0 if sort_by is None else 1
        sorted_ind = argsort(list(zip(*measurements_reduced))[sort_by_idx])
        if sort_desc:
            sorted_ind = reversed(sorted_ind)

        if crossvalid_reduce:
            measurements = measurements_reduced
    else:   # single validation results
        if len(tuples[0]) != 2:
            raise ValueError('invalid evaluation results passed')

        params, metric_results = list(zip(*tuples))
        if sort_by:
            sorted_ind = argsort([r[sort_by] for r in metric_results])
        else:
            sorted_ind = argsort(params)

        if sort_desc:
            sorted_ind = reversed(sorted_ind)

        measurements = tuples

    return [measurements[i] for i in sorted_ind]


def get_doc_lengths(dtm):
    if isinstance(dtm, np.matrix):
        dtm = dtm.A
    if dtm.ndim != 2:
        raise ValueError('`dtm` must be a 2D array/matrix')

    res = np.sum(dtm, axis=1)
    if res.ndim != 1:
        return res.A.flatten()
    else:
        return res


def get_doc_frequencies(dtm, min_val=1, proportions=False):
    """
    For each word in the vocab of `dtm` (i.e. its columns), return how often it occurs at least `min_val` times.
    If `proportions` is True, return proportions scaled to the number of documents instead of absolute numbers.
    """
    if dtm.ndim != 2:
        raise ValueError('`dtm` must be a 2D array/matrix')

    doc_freq = np.sum(dtm >= min_val, axis=0)

    if doc_freq.ndim != 1:
        doc_freq = doc_freq.A.flatten()

    if proportions:
        return doc_freq / dtm.shape[0]
    else:
        return doc_freq


def get_codoc_frequencies(dtm, min_val=1, proportions=False):
    """
    For each unique pair of words `w1, w2` in the vocab of `dtm` (i.e. its columns), return how often both occur
    together at least `min_val` times. If `proportions` is True, return proportions scaled to the number of documents
    instead of absolute numbers.
    """
    if dtm.ndim != 2:
        raise ValueError('`dtm` must be a 2D array/matrix')

    n_docs, n_vocab = dtm.shape
    if n_vocab < 2:
        raise ValueError('`dtm` must have at least two columns (i.e. 2 unique words)')

    word_in_doc = dtm >= min_val

    codoc_freq = {}
    for w1, w2 in itertools.combinations(range(n_vocab), 2):
        if issparse(dtm):
            w1_in_docs = word_in_doc[:, w1].A.flatten()
            w2_in_docs = word_in_doc[:, w2].A.flatten()
        else:
            w1_in_docs = word_in_doc[:, w1]
            w2_in_docs = word_in_doc[:, w2]

        freq = np.sum(w1_in_docs & w2_in_docs)
        if proportions:
            freq /= n_docs
        codoc_freq[(w1, w2)] = freq

    return codoc_freq


def get_term_frequencies(dtm):
    if isinstance(dtm, np.matrix):
        dtm = dtm.A
    if dtm.ndim != 2:
        raise ValueError('`dtm` must be a 2D array/matrix')

    res = np.sum(dtm, axis=0)
    if res.ndim != 1:
        return res.A.flatten()
    else:
        return res


def get_term_proportions(dtm):
    """
    Return the term proportions given the document-term matrix `dtm`
    """
    unnorm = get_term_frequencies(dtm)
    return unnorm / unnorm.sum()


def get_marginal_topic_distrib(doc_topic_distrib, doc_lengths):
    """
    Return marginal topic distribution p(T) (topic proportions) given the document-topic distribution (theta)
    `doc_topic_distrib` and the document lengths `doc_lengths`. The latter can be calculated with `get_doc_lengths()`.
    """
    unnorm = (doc_topic_distrib.T * doc_lengths).sum(axis=1)
    return unnorm / unnorm.sum()


def get_marginal_word_distrib(topic_word_distrib, p_t):
    """
    Return the marginal word distribution p(w) (term proportions derived from topic model) given the
    topic-word distribution (phi) `topic_word_distrib` and the marginal topic distribution p(T) `p_t`.
    The latter can be calculated with `get_marginal_topic_distrib()`.
    """
    return (topic_word_distrib.T * p_t).sum(axis=1)


def get_word_distinctiveness(topic_word_distrib, p_t):
    """
    Calculate word distinctiveness according to Chuang et al. 2012.
    distinctiveness(w) = KL(P(T|w), P(T)) = sum_T(P(T|w) log(P(T|w)/P(T)))
    with P(T) .. marginal topic distribution
         P(T|w) .. prob. of a topic given a word
    """
    topic_given_w = topic_word_distrib / topic_word_distrib.sum(axis=0)
    return (topic_given_w * np.log(topic_given_w.T / p_t).T).sum(axis=0)


def get_word_saliency(topic_word_distrib, doc_topic_distrib, doc_lengths):
    """
    Calculate word saliency according to Chuang et al. 2012.
    saliency(w) = p(w) * distinctiveness(w)
    """
    p_t = get_marginal_topic_distrib(doc_topic_distrib, doc_lengths)
    p_w = get_marginal_word_distrib(topic_word_distrib, p_t)

    return p_w * get_word_distinctiveness(topic_word_distrib, p_t)


def _words_by_score(words, score, least_to_most, n=None):
    """
    Order a vector of `words` by a `score`, either `least_to_most` or reverse. Optionally return only the top `n`
    results.
    """
    if words.shape != score.shape:
        raise ValueError('`words` and `score` must have the same shape')

    if n is not None and (n <= 0 or n > len(words)):
        raise ValueError('`n` must be in range [0, len(words)]')

    indices = np.argsort(score)
    if not least_to_most:
        indices = indices[::-1]

    ordered_words = words[indices]

    if n is not None:
        return ordered_words[:n]
    else:
        return ordered_words


def _words_by_salience_score(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n=None, least_to_most=False):
    """Return words in `vocab` ordered by saliency score."""
    saliency = get_word_saliency(topic_word_distrib, doc_topic_distrib, doc_lengths)
    return _words_by_score(vocab, saliency, least_to_most=least_to_most, n=n)


def get_most_salient_words(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n=None):
    """
    Order the words from `vocab` by "saliency score" (Chuang et al. 2012) from most to least salient. Optionally only
    return the `n` most salient words.
    """
    return _words_by_salience_score(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n)


def get_least_salient_words(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n=None):
    """
    Order the words from `vocab` by "saliency score" (Chuang et al. 2012) from least to most salient. Optionally only
    return the `n` least salient words.
    """
    return _words_by_salience_score(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n, least_to_most=True)


def _words_by_distinctiveness_score(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n=None,
                                    least_to_most=False):
    """Return words in `vocab` ordered by distinctiveness score."""
    p_t = get_marginal_topic_distrib(doc_topic_distrib, doc_lengths)
    distinct = get_word_distinctiveness(topic_word_distrib, p_t)

    return _words_by_score(vocab, distinct, least_to_most=least_to_most, n=n)


def get_most_distinct_words(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n=None):
    """
    Order the words from `vocab` by "distinctiveness score" (Chuang et al. 2012) from most to least distinctive.
    Optionally only return the `n` most distinctive words.
    """
    return _words_by_distinctiveness_score(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n)


def get_least_distinct_words(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n=None):
    """
    Order the words from `vocab` by "distinctiveness score" (Chuang et al. 2012) from least to most distinctive.
    Optionally only return the `n` least distinctive words.
    """
    return _words_by_distinctiveness_score(vocab, topic_word_distrib, doc_topic_distrib, doc_lengths, n,
                                           least_to_most=True)


def get_topic_word_relevance(topic_word_distrib, doc_topic_distrib, doc_lengths, lambda_):
    """
    Calculate the topic-word relevance score with a lambda parameter `lambda_` according to Sievert and Shirley 2014.
    relevance(w,T|lambda) = lambda * log phi_{w,t} + (1-lambda) * log (phi_{w,t} / p(w))
    with phi  .. topic-word distribution
         p(w) .. marginal word probability
    """
    p_t = get_marginal_topic_distrib(doc_topic_distrib, doc_lengths)
    p_w = get_marginal_word_distrib(topic_word_distrib, p_t)

    logtw = np.log(topic_word_distrib)
    loglift = np.log(topic_word_distrib / p_w)

    return lambda_ * logtw + (1-lambda_) * loglift


def _check_relevant_words_for_topic_args(vocab, rel_mat, topic):
    if rel_mat.ndim != 2:
        raise ValueError('`rel_mat` must be a 2D array or matrix')

    if len(vocab) != rel_mat.shape[1]:
        raise ValueError('the length of the `vocab` array must match the number of columns in `rel_mat`')

    if not 0 <= topic < rel_mat.shape[0]:
        raise ValueError('`topic` must be a topic index in range [0,%d)' % rel_mat.shape[0])


def get_most_relevant_words_for_topic(vocab, rel_mat, topic, n=None):
    """
    Get words from `vocab` for `topic` ordered by most to least relevance (Sievert and Shirley 2014) using the relevance
    matrix `rel_mat` obtained from `get_topic_word_relevance()`.
    Optionally only return the `n` most relevant words.
    """
    _check_relevant_words_for_topic_args(vocab, rel_mat, topic)
    return _words_by_score(vocab, rel_mat[topic], least_to_most=False, n=n)


def get_least_relevant_words_for_topic(vocab, rel_mat, topic, n=None):
    """
    Get words from `vocab` for `topic` ordered by least to most relevance (Sievert and Shirley 2014) using the relevance
    matrix `rel_mat` obtained from `get_topic_word_relevance()`.
    Optionally only return the `n` least relevant words.
    """
    _check_relevant_words_for_topic_args(vocab, rel_mat, topic)
    return _words_by_score(vocab, rel_mat[topic], least_to_most=True, n=n)


def generate_topic_labels_from_top_words(topic_word_distrib, doc_topic_distrib, doc_lengths, vocab,
                                         n_words=None, lambda_=1, labels_glue='_', labels_format='{i1}_{topwords}'):
    """
    Generate topic labels derived from the top words of each topic. The top words are determined from the
    relevance score (Sievert and Shirley 2014) depending on `lambda_`. Specify the number of top words in the label
    with `n_words`. If `n_words` is None, a minimum number of words will be used to create unique labels for each
    topic. Topic labels are formed by joining the top words with `labels_glue` and formatting them with
    `labels_format`. Placeholders in `labels_format` are `{i0}` (zero-based topic index),
    `{i1}` (one-based topic index) and `{topwords}` (top words glued with `labels_glue`).
    """
    rel_mat = get_topic_word_relevance(topic_word_distrib, doc_topic_distrib, doc_lengths, lambda_=lambda_)

    if n_words is None:
        n_words = range(1, len(vocab)+1)
    else:
        if not 1 <= n_words <= len(vocab):
            raise ValueError('`n_words` must be in range [1, %d]' % len(vocab))

        n_words = range(n_words, n_words+1)

    most_rel_words = [tuple(get_most_relevant_words_for_topic(vocab, rel_mat, t))
                      for t in range(topic_word_distrib.shape[0])]

    n_most_rel = []
    for n in n_words:
        n_most_rel = [ws[:n] for ws in most_rel_words]
        if len(n_most_rel) == len(set(n_most_rel)):   # we have a list of unique word sequences
            break

    assert n_most_rel

    topic_labels = [labels_format.format(i0=i, i1=i+1, topwords=labels_glue.join(ws))
                    for i, ws in enumerate(n_most_rel)]

    if len(topic_labels) != len(set(topic_labels)):
        raise ValueError('generated labels are not unique')

    return topic_labels


def parameters_for_ldavis(topic_word_distrib, doc_topic_distrib, dtm, vocab, sort_topics=False):
    return dict(
        topic_term_dists=topic_word_distrib,
        doc_topic_dists=doc_topic_distrib,
        vocab=vocab,
        doc_lengths=get_doc_lengths(dtm),
        term_frequency=get_term_frequencies(dtm),
        sort_topics=sort_topics,
    )


def merge_params(varying_parameters, constant_parameters):
    if not varying_parameters:
        return [constant_parameters]

    merged_params = []
    for p in varying_parameters:
        m = p.copy()
        m.update(constant_parameters)
        merged_params.append(m)

    return merged_params


def get_split_folds_array(folds, size):
    #each = int(round(size / folds))
    each = size // folds
    folds_arr = np.repeat(np.arange(0, folds), np.repeat(each, folds))

    assert len(folds_arr) <= size

    if len(folds_arr) < size:
        folds_arr = np.concatenate((folds_arr, np.random.randint(0, folds, size-len(folds_arr))))

    assert len(folds_arr) == size
    assert min(folds_arr) == 0
    assert max(folds_arr) == folds - 1

    np.random.shuffle(folds_arr)

    return folds_arr


class MultiprocModelsRunner(object):
    def __init__(self, worker_class, data, varying_parameters=None, constant_parameters=None, n_max_processes=None):
        self.tasks_queues = None
        self.results_queue = None
        self.workers = None

        n_max_processes = n_max_processes or mp.cpu_count()
        if n_max_processes < 1:
            raise ValueError('`n_max_processes` must be at least 1')

        varying_parameters = varying_parameters or []
        n_varying_params = len(varying_parameters)

        self.worker_class = worker_class

        self.varying_parameters = varying_parameters
        self.constant_parameters = constant_parameters or {}

        self.got_named_docs = isinstance(data, dict)
        if self.got_named_docs:
            self.data = {doc_label: self._prepare_sparse_data(doc_data) for doc_label, doc_data in data.items()}
        else:
            self.data = {None: self._prepare_sparse_data(data)}

        self.n_workers = min(max(1, n_varying_params) * len(self.data), n_max_processes)

        logger.info('init with %d workers' % self.n_workers)

        atexit.register(self.shutdown_workers)

    def __del__(self):
        """destructor. shutdown all workers"""
        self.shutdown_workers()

    def shutdown_workers(self):
        if not self.workers:
            return

        logger.info('sending shutdown signal to workers')

        [q.put(None) for q in self.tasks_queues]   # `None` is the shutdown signal
        [q.join() for q in self.tasks_queues]

        [w.join() for w in self.workers]

        self.tasks_queues = None
        self.results_queue = None
        self.workers = None
        self.n_workers = 0

    def run(self):
        self._setup_workers(self.worker_class)

        params = merge_params(self.varying_parameters, self.constant_parameters)
        n_params = len(params)
        docs = list(self.data.keys())
        n_docs = len(docs)
        if n_params == 0:
            tasks = list(zip(docs, [{}] * n_docs))
        else:
            tasks = list(itertools.product(docs, params))
        n_tasks = len(tasks)
        logger.info('multiproc models: starting with %d parameter sets on %d documents (= %d tasks) and %d processes'
                    % (n_params, n_docs, n_tasks, self.n_workers))

        logger.debug('distributing initial work')
        task_idx = 0
        for d, p in tasks[:self.n_workers]:
            logger.debug('> sending task %d/%d to worker %d' % (task_idx + 1, n_tasks, task_idx))
            self.tasks_queues[task_idx].put((d, p))
            task_idx += 1

        worker_results = []
        while task_idx < n_tasks:
            logger.debug('awaiting result')
            finished_worker, w_doc, w_params, w_result = self.results_queue.get()    # blocking
            logger.debug('> got result from worker %d' % finished_worker)

            worker_results.append((w_doc, w_params, w_result))

            d, p = tasks[task_idx]
            logger.debug('> sending task %d/%d to worker %d' % (task_idx + 1, n_tasks, finished_worker))
            self.tasks_queues[finished_worker].put((d, p))
            task_idx += 1

        logger.debug('awaiting final results')
        [q.join() for q in self.tasks_queues]   # block for last submitted tasks

        for _ in range(self.n_workers):
            _, w_doc, w_params, w_result = self.results_queue.get()  # blocking
            worker_results.append((w_doc, w_params, w_result))

        logger.info('multiproc models: finished')

        self.shutdown_workers()

        if self.got_named_docs:
            res = defaultdict(list)
            for d, p, r in worker_results:
                res[d].append((p, r))
            return res
        else:
            _, p, r = zip(*worker_results)
            return list(zip(p, r))

    def _setup_workers(self, worker_class):
        self.tasks_queues = []
        self.results_queue = mp.Queue()
        self.workers = []

        for i in range(self.n_workers):
            task_q = mp.JoinableQueue()
            w = self._new_worker(worker_class, i, task_q, self.results_queue, self.data)
            w.start()

            self.workers.append(w)
            self.tasks_queues.append(task_q)

    def _new_worker(self, worker_class, i, task_queue, results_queue, data):
        return worker_class(i, task_queue, results_queue, data, name='%s#%d' % (str(worker_class), i))

    @staticmethod
    def _prepare_sparse_data(data):
        if not hasattr(data, 'dtype') or not hasattr(data, 'shape') or len(data.shape) != 2:
            raise ValueError('`data` must be a NumPy array/matrix or SciPy sparse matrix of two dimensions')

        if data.dtype == np.int:
            arr_ctype = ctypes.c_int
        elif data.dtype == np.int32:
            arr_ctype = ctypes.c_int32
        elif data.dtype == np.int64:
            arr_ctype = ctypes.c_int64
        else:
            raise ValueError('dtype of `data` is not supported: `%s`' % data.dtype)

        if not hasattr(data, 'format'):  # dense matrix -> convert to sparse matrix in coo format
            data = coo_matrix(data)
        elif data.format != 'coo':
            data = data.tocoo()

        sparse_data_base = mp.Array(arr_ctype, data.data)
        sparse_rows_base = mp.Array(ctypes.c_int, data.row)  # TODO: datatype correct?
        sparse_cols_base = mp.Array(ctypes.c_int, data.col)  # TODO: datatype correct?

        logger.info('initializing evaluation with sparse matrix of format `%s` and shape %dx%d'
                    % (data.format, data.shape[0], data.shape[1]))

        return sparse_data_base, sparse_rows_base, sparse_cols_base


class MultiprocModelsWorkerABC(mp.Process):
    package_name = None   # abstract. override in subclass

    def __init__(self, worker_id, tasks_queue, results_queue, data,
                 group=None, target=None, name=None, args=(), kwargs=None):
        super(MultiprocModelsWorkerABC, self).__init__(group, target, name, args, kwargs or {})

        logger.debug('worker `%s`: creating worker with ID %d' % (self.name, worker_id))
        self.worker_id = worker_id
        self.tasks_queue = tasks_queue
        self.results_queue = results_queue

        self.data_per_doc = {}
        for doc_label, sparse_mem in data.items():
            sparse_data_base, sparse_row_ind_base, sparse_col_ind_base = sparse_mem
            sparse_data = np.ctypeslib.as_array(sparse_data_base.get_obj())
            sparse_row_ind = np.ctypeslib.as_array(sparse_row_ind_base.get_obj())
            sparse_col_ind = np.ctypeslib.as_array(sparse_col_ind_base.get_obj())
            logger.debug('worker `%s`: creating sparse data matrix for document `%s`' % (self.name, doc_label))
            self.data_per_doc[doc_label] = coo_matrix((sparse_data, (sparse_row_ind, sparse_col_ind)))

    def run(self):
        logger.debug('worker `%s`: run' % self.name)

        for doc, params in iter(self.tasks_queue.get, None):
            logger.debug('worker `%s`: received task' % self.name)

            data = self.data_per_doc[doc]
            logger.info('fitting LDA model from package `%s` to data `%s` of shape %s with parameters:'
                        ' %s' % (self.package_name, doc, data.shape, params))

            results = self.fit_model(data, params)
            self.send_results(doc, params, results)
            self.tasks_queue.task_done()

        logger.debug('worker `%s`: shutting down' % self.name)
        self.tasks_queue.task_done()

    def fit_model(self, data, params):
        raise NotImplementedError('abstract base class method `fit_model` needs to be defined')

    def send_results(self, doc, params, results):
        self.results_queue.put((self.worker_id, doc, params, results))


class MultiprocEvaluationRunner(MultiprocModelsRunner):
    def __init__(self, worker_class, available_metrics, data, varying_parameters, constant_parameters=None,
                 metric=None, metric_options=None, n_max_processes=None, return_models=False):  # , n_folds=0
        if isinstance(data, dict):
            raise ValueError('`data` cannot be a dict for evaluation')

        super(MultiprocEvaluationRunner, self).__init__(worker_class, data, varying_parameters, constant_parameters,
                                                        n_max_processes)

        if len(self.varying_parameters) < 1:
            raise ValueError('`varying_parameters` must contain at least one value')

        if type(available_metrics) not in (list, tuple) or not available_metrics:
            raise ValueError('`available_metrics` must be a list or tuple with a least one element')

        # if metric == 'cross_validation' and n_folds <= 1:
        #     raise ValueError('`n_folds` must be at least 2 if `metric` is set to "cross_validation"')
        # elif n_folds > 1 and metric not in (None, 'cross_validation'):
        #     raise ValueError('`metric` must be set to "cross_validation" if `n_folds` is greater than 1')

        # if metric is None:
        #     if n_folds <= 1:
        #         metric = available_metrics  # use all metrics
        #     else:
        #         metric = 'cross_validation'

        metric = metric or available_metrics

        if metric_options is None:
            metric_options = {}

        if type(metric) not in (list, tuple):
            metric = [metric]

        if type(metric) not in (list, tuple) or not metric:
            raise ValueError('`metric` must be a list or tuple with a least one element')

        for m in metric:
            if m not in available_metrics:
                raise ValueError('invalid metric was passed: "%s". valid metrics: %s' % (m, available_metrics))

        # currently not supported any more:
        # self.n_folds = max(n_folds, 0)
        # if self.n_folds > 1:
        #     self.split_folds = get_split_folds_array(n_folds, data.shape[0])
        # else:
        #     self.split_folds = None

        self.eval_metric = metric
        self.eval_metric_options = metric_options or {}
        self.return_models = return_models

    def _new_worker(self, worker_class, i, task_queue, results_queue, data):
        return worker_class(i, self.eval_metric, self.eval_metric_options, self.return_models,
                            task_queue, results_queue, data, name='%s#%d' % (str(worker_class), i))


class MultiprocEvaluationWorkerABC(MultiprocModelsWorkerABC):
    def __init__(self, worker_id,
                 eval_metric, eval_metric_options, return_models,
                 tasks_queue, results_queue, data,
                 group=None, target=None, name=None, args=(), kwargs=None):
        super(MultiprocEvaluationWorkerABC, self).__init__(worker_id,
                                                           tasks_queue, results_queue, data,
                                                           group, target, name, args, kwargs)
        self.eval_metric = eval_metric
        self.eval_metric_options = eval_metric_options
        self.return_models = return_models
