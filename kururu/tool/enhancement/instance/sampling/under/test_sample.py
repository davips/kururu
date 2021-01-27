from unittest import TestCase

from aiuna import Root
from aiuna.step.dataset import Dataset
from kururu import AutoIns
from kururu.tool.enhancement.instance.sampling.under.sample import Sample_, Sample


class TestSample(TestCase):
    def test__rus_(self):
        samplediris = Root >> (Dataset() * Sample_(n=120))
        self.assertEqual(120, len(samplediris.X))

    def test__rus(self):
        samplediris =  Root >> (Dataset() * Sample_(n=140))
        self.assertEqual(140, len((samplediris >> AutoIns * Sample).X))  # TODO: inhibit UserWarning
        self.assertEqual(100, len((samplediris >> AutoIns * Sample).inner.X))
