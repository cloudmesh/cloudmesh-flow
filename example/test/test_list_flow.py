from unittest import TestCase
import webbrowser

class Test_Visualize(TestCase):
    def test_list_flow(self):
        flow_name = "testflow2-flow"
        url = "http://127.0.0.1:8080/flow/monitor/" + flow_name
        webbrowser.open(url)


