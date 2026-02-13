from typing import Iterable, List
import logging
import numpy as np
from sentence_transformers import SentenceTransformer
from ..core.interfaces import Embedder

logger = logging.getLogger(__name__)


class SentenceEmbedder(Embedder):
    """Embedder using `sentence-transformers`.

    This class is pluggable and implements a simple `embed` method returning
    lists of floats.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        logger.info("Loading embedder model: %s", model_name)
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: Iterable[str]) -> List[List[float]]:
        arr = self.model.encode(list(texts), show_progress_bar=False)
        # ensure Python lists for serialization
        return [list(map(float, row)) for row in np.array(arr)]
