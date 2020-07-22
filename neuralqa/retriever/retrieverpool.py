
from neuralqa.retriever import ElasticSearchRetriever
import logging

logger = logging.getLogger(__name__)


class RetrieverPool():
    def __init__(self, retrievers):

        self.retriever_pool = {}
        for retriever in retrievers["options"]:
            if (retriever["type"] == "elasticsearch"):
                self.retriever_pool[retriever["value"]] = ElasticSearchRetriever(
                    host=retriever["host"], port=retriever["port"], body_field=retriever["fields"]["body_field"],
                    secondary_fields=retriever["fields"]["secondary_fields"])
            if (retriever["type"] == "solr"):
                logger.info("We do not yet support Solr retrievers")
        self.selected_retriever = retrievers["selected"]

    @property
    def retriever(self):
        return self.retriever_pool[self.selected_retriever]

    @property
    def selected_retriever(self):
        return self._selected_retriever

    @selected_retriever.setter
    def selected_retriever(self, selected_retriever):
        if (selected_retriever in self.retriever_pool):
            self._selected_retriever = selected_retriever
        else:
            default_retriever = next(iter(self.retriever_pool))
            logger.info(
                ">> Retriever you are attempting to use %s does not exist in retriever pool. Using the following default retriever instead %s ", selected_retriever, default_retriever)
            self._selected_retriever = default_retriever
