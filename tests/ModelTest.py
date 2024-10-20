import unittest
from PyQt5.QtGui import QStandardItem
import Model

class MyTestCase(unittest.TestCase):
    def test_tableModel(self):
        tm = Model.ProjectModel("../settingsTest/projectCockpit.json")
        self.assertEqual(3, tm.rowCount(parent=None))
        self.assertEqual(3, tm.columnCount(parent=None))
        link = tm.getLinkList()[0]
        self.assertEqual("Homepage Bastelecke", link["name"])
        self.assertEqual("starter", link["type"])

    def test_model_init(self):
        m = Model.Model("../settingsTest/settings.json")
        # check starters list
        self.assertEqual("Explorer", m.starters[0]["name"])

        # check projects
        #print(m.projects)
        self.assertEqual("COCKPIT", m.projects[0].getName())

    def test_model_getProjectByIndex(self):
        m = Model.Model("../settingsTest/settings.json")
        p = m.getProjectByIndex(0)
        # check starters list
        self.assertIsInstance(p, QStandardItem)

    def test_model_getStarterNames(self):
        m = Model.Model("../settingsTest/settings.json")
        s = m.getStarterNames()
        # check starters list
        self.assertIsInstance(s, list)
        self.assertEqual("Explorer",s[0])

    def test_model_getLinkFromName(self):
        m = Model.Model("../settingsTest/settings.json")
        l = m.getLinkFromName("Homepage Bastelecke")
        self.assertEqual("Homepage Bastelecke",l["name"])

    def test_model_getProjects(self):
        m = Model.Model("../settingsTest/settings.json")
        p = m.getProjects()
        self.assertEqual("./icons/unknown.png", p[0]["icon"])
        self.assertEqual("COCKPIT", p[0]["name"])

    def test_model_addProjectEntry(self):
        m = Model.Model("../settingsTest/settings.json")
        d = dict()
        d["name"] = "Test"
        d["description"] = "xxx"
        d["type"] = "http"
        d["url"] = "https://www.thingiverse.com/"
        m.addLinkCurrentProject(d)
        links = m.getLinksForCurrentProject()
        self.assertEqual(4, len(links))
        self.assertEqual("Test", links[3]["name"])
        self.assertEqual("xxx", links[3]["description"])
        self.assertEqual("http", links[3]["type"])
        self.assertEqual("https://www.thingiverse.com/", links[3]["url"])
        m.getCurrentProject().deleteLinkEntry(3)
        self.assertEqual(3, len(links))

        index = 1
        m.addLinkCurrentProject(d, index)
        links = m.getLinksForCurrentProject()
        self.assertEqual(4, len(links))
        self.assertEqual("Test", links[index]["name"])
        self.assertEqual("xxx", links[index]["description"])
        self.assertEqual("http", links[index]["type"])
        self.assertEqual("https://www.thingiverse.com/", links[index]["url"])
        m.getCurrentProject().deleteLinkEntry(index)
        self.assertEqual(3, len(links))


if __name__ == '__main__':
    unittest.main()
