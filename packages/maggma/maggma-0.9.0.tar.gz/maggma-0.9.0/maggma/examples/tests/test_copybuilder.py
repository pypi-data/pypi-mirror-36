"""Test maggma.examples.builders.CopyBuilder."""

import logging
from datetime import datetime, timedelta
from unittest import TestCase
from uuid import uuid4

from maggma.stores import MongoStore
from maggma.runner import Runner
from maggma.examples.builders import CopyBuilder


class TestCopyBuilder(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dbname = "test_" + uuid4().hex
        s = MongoStore(cls.dbname, "test")
        s.connect()
        cls.client = s.collection.database.client

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database(cls.dbname)

    def setUp(self):
        tic = datetime.now()
        toc = tic + timedelta(seconds=1)
        keys = list(range(20))
        self.old_docs = [{"lu": tic, "k": k, "v": "old"}
                         for k in keys]
        self.new_docs = [{"lu": toc, "k": k, "v": "new"}
                         for k in keys[:10]]
        kwargs = dict(key="k", lu_field="lu")
        self.source = MongoStore(self.dbname, "source", **kwargs)
        self.target = MongoStore(self.dbname, "target", **kwargs)
        self.builder = CopyBuilder(self.source, self.target)
        self.source.connect()
        self.source.collection.create_index(
            [(self.source.lu_field, -1), (self.source.key, 1)])
        self.target.connect()
        self.target.collection.create_index(
            [(self.target.lu_field, -1), (self.target.key, 1)])
        self.target.collection.create_index(self.target.key)

    def tearDown(self):
        self.source.collection.drop()
        self.target.collection.drop()

    def test_get_items(self):
        self.source.collection.insert_many(self.old_docs)
        self.assertEqual(len(list(self.builder.get_items())),
                         len(self.old_docs))
        self.target.collection.insert_many(self.old_docs)
        self.assertEqual(len(list(self.builder.get_items())), 0)
        self.source.update(self.new_docs, update_lu=False)
        self.assertEqual(len(list(self.builder.get_items())),
                         len(self.new_docs))

    def test_process_item(self):
        self.source.collection.insert_many(self.old_docs)
        items = list(self.builder.get_items())
        self.assertCountEqual(items, map(self.builder.process_item, items))

    def test_update_targets(self):
        self.source.collection.insert_many(self.old_docs)
        self.source.update(self.new_docs, update_lu=False)
        self.target.collection.insert_many(self.old_docs)
        items = list(map(self.builder.process_item, self.builder.get_items()))
        self.builder.update_targets(items)
        self.assertEqual(self.target.query_one(criteria={"k": 0})["v"], "new")
        self.assertEqual(self.target.query_one(criteria={"k": 10})["v"], "old")

    def test_index_warning(self):
        """Should log warning when recommended store indexes are not present."""
        self.source.collection.drop_index("lu_-1_k_1")
        with self.assertLogs(level=logging.WARNING) as cm:
            self.builder.get_items()
        self.assertIn("Ensure indices", "\n".join(cm.output))
        self.source.collection.create_index("lu_-1_k_1")

    def test_runner(self):
        self.source.collection.insert_many(self.old_docs)
        self.source.update(self.new_docs, update_lu=False)
        self.target.collection.insert_many(self.old_docs)
        runner = Runner([self.builder])
        runner.run()
        self.assertEqual(self.target.query_one(criteria={"k": 0})["v"], "new")
        self.assertEqual(self.target.query_one(criteria={"k": 10})["v"], "old")

    def test_query(self):
        self.builder.query = {"k": {"$gt": 5}}
        self.source.collection.insert_many(self.old_docs)
        self.source.update(self.new_docs, update_lu=False)
        runner = Runner([self.builder])
        runner.run()
        all_docs = list(self.target.query(criteria={}))
        self.assertEqual(len(all_docs), 14)
        self.assertTrue(min([d['k'] for d in all_docs]), 6)
