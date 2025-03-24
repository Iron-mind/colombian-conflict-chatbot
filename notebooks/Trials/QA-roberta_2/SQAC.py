# Loading script for the SQAC dataset.
import json
import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = """
bibtex
@article{DBLP:journals/corr/abs-2107-07253,
  author    = {Asier Guti{\'{e}}rrez{-}Fandi{\~{n}}o and
               Jordi Armengol{-}Estap{\'{e}} and
               Marc P{\`{a}}mies and
               Joan Llop{-}Palao and
               Joaqu{\'{\i}}n Silveira{-}Ocampo and
               Casimiro Pio Carrino and
               Aitor Gonzalez{-}Agirre and
               Carme Armentano{-}Oller and
               Carlos Rodr{\'{\i}}guez Penagos and
               Marta Villegas},
  title     = {Spanish Language Models},
  journal   = {CoRR},
  volume    = {abs/2107.07253},
  year      = {2021},
  url       = {https://arxiv.org/abs/2107.07253},
  archivePrefix = {arXiv},
  eprint    = {2107.07253},
  timestamp = {Wed, 21 Jul 2021 15:55:35 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2107-07253.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
            """

_DESCRIPTION = """
This dataset contains 6,247 contexts and 18,817 questions with their answers, 1 to 5 for each fragment.

The sources of the contexts are:

* Encyclopedic articles from [Wikipedia in Spanish](https://es.wikipedia.org/), used under [CC-by-sa licence](https://creativecommons.org/licenses/by-sa/3.0/legalcode). 

* News from [Wikinews in Spanish](https://es.wikinews.org/), used under [CC-by licence](https://creativecommons.org/licenses/by/2.5/). 

* Text from the Spanish corpus [AnCora](http://clic.ub.edu/corpus/en), which is a mix from diferent newswire and literature sources, used under [CC-by licence] (https://creativecommons.org/licenses/by/4.0/legalcode). 

This dataset can be used to build extractive-QA.
               """

_HOMEPAGE = """"""

_URL = "data-QA/"
_TRAINING_FILE = "train.json"
_DEV_FILE = "dev.json"
_TEST_FILE = "test.json"


class SQACConfig(datasets.BuilderConfig):
    """ Builder config for the SQAC dataset """

    def __init__(self, **kwargs):
        """BuilderConfig for SQAC.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SQACConfig, self).__init__(**kwargs)


class SQAC(datasets.GeneratorBasedBuilder):
    """SQAC Dataset."""

    BUILDER_CONFIGS = [
        SQACConfig(
            name="SQAC",
            #version=datasets.Version("1.0.1"),
            description="SQAC dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            sqac_data = json.load(f)
            for article in sqac_data["data"]:
                title = article.get("title", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
