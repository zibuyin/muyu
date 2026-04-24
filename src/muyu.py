import rumps
import threading
import time
import backend
import graph as graph

counterNumber = 0


class muyuApp (rumps.App):
    def __init__ (self, name="muyu", title=f"⌨️ {counterNumber}", icon=None, template=None, menu=None, quit_button='Quit'):
        super().__init__(name, title, icon, template, menu, quit_button)
        self.total = -1
        
        self.menu = [
            "Made by Nathan Yin",
            None
        ]
        backend.init()
    
    @rumps.timer(0.1)
    def updateCounter(self, _):
            parsed_db = backend.getDB()
            self.total = parsed_db["total"]
            # print(f"BBG: {self.total}")
            self.updateCounterUi(self)
            self.updateKeypressUi(self)
    
    @rumps.clicked("Show Graph")
    def graphBtn(self, _):
         graph.plotKeyboard(backend.getDB())
    
    @rumps.clicked("Clear Data")
    def clearDB(self, _):
         backend.clearDB()
         rumps.notification("DB Cleared!", "The counter has reset!","")

    # @rumps.clicked("Turn on sounds")
    def updateCounterUi(self, _):
        parsedTitle = "⌨️ " + str(self.total)
        self.title = parsedTitle

    def updateKeypressUi(self, _):
         pass
if __name__ == "__main__":
    muyuApp().run()