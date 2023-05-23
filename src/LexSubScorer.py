class LexSubScorer:
    @staticmethod
    def add_measure(cosine_similarity, substitute, target, contexts):
        sub_to_tar_similarity = cosine_similarity(substitute, target)
        sub_to_con_similarity = 0
        for context in contexts:
            sub_to_con_similarity += cosine_similarity(substitute, context)
        return (sub_to_tar_similarity + sub_to_con_similarity) / (len(contexts) + 1)
    
    @staticmethod
    def bal_add_measure(cosine_similarity, substitute, target, contexts):
        sub_to_tar_similarity = cosine_similarity(substitute, target)
        sub_to_con_similarity = 0
        for context in contexts:
            sub_to_con_similarity += cosine_similarity(substitute, context)
        return (len(contexts) * sub_to_tar_similarity + sub_to_con_similarity) / (len(contexts) * 2)

    @staticmethod
    def mult_measure(cosine_similarity, substitute, target, contexts):
        sub_to_tar_similarity = cosine_similarity(substitute, target)
        sub_to_con_similarity = 1
        for context in contexts:
            sub_to_con_similarity *= cosine_similarity(substitute, context)
        return (sub_to_tar_similarity * sub_to_con_similarity) ** (1 / (len(contexts) + 1))

    @staticmethod
    def bal_mult_measure(cosine_similarity, substitute, target, contexts):
        sub_to_tar_similarity = cosine_similarity(substitute, target)
        sub_to_con_similarity = 1
        for context in contexts:
            sub_to_con_similarity *= cosine_similarity(substitute, context)
        return (sub_to_tar_similarity ** len(contexts) * sub_to_con_similarity) ** (1 / (len(contexts) * 2))
