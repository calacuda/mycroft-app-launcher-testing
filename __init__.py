from adapt.intent import IntentBuilder 
from mycroft import MycroftSkill, intent_handler
from os import system as run
from json import loads as json_reader


class Launcher(MycroftSkill):

    def __init__(self):
        super().__init__()
        #self.initialize()
        #self.apps = self.settings
        
    def initialize(self):
        run("notify-send 'debug' 'initializing'")
        self.register_entity_file("app.entity")
        run("notify-send 'debug' 'registered entity file'")
        #self.register_entity_file("lang.entity")
        self.white_list = json_reader(self.settings.get("white list").replace("'", '"'))
        run(f"notify-send 'whitelist' '{self.white_list}'")
        self.repls = json_reader(self.settings.get("REPLs").replace("'", '"'))
        run(f"notify-send 'repls' '{self.repls}'")
        self.register_intent_file("launch.intent", self.handle_launch_intent)
        #self.apps = self.settings
        
    def equivilency(self, app_name):
        if app_name in {"web browser", "browser", "google", "google machine", "internet", "internet program"}:
            return "browser"
        elif app_name in {"terminal", "terminals", "prompt", "prompts", "command prompt", "command prompts", "CLI", "CLI's"}:
            return "terminal"
        elif app_name == "minecraft":
            return "minecraft-launcher"
        else:
            return app_name

    def get_target_app(self, app_title):
        app_name = self.equivilency(app_title.lower())
        white_list_names = self.white_list.keys() #self.settings.get("white list").split(",")
        if app_name in self.settings.keys():
            return self.settings.get(app_title)
        #elif app_title not in white_list and app_title not in self.settings.keys():
        #    return 1
        elif (app_title in white_list):
            return self.white_list.get(app_title)
        elif (app_name in white_list):
            return self.white_list.get(app_name)
        else:
            return 1
        
    @intent_handler("launch.intent")
    def handle_launch_intent(self, app):
        """
        the main hadeller
        """
        application = self.get_target_app(app.data.get("app")) # self.settings.get(self.equivilency(app.data.get("app")))
        self.acknowledge()
        if application in self.repls.keys():
            self.open_repl(self.repls.get(application))
        elif application != 1:
            try:
                run(f'notify-send "Running" "{application}"')
                run(application)
            except:
                self.speak("bruh... I can't do that.")
                run(f'echo "got error when running :  {app.__dict__}\nsettings :  {type(self.settings)}\nsettings :  {self.settings}" > ~/mycroft_launcher_error.txt')
                run(f'notify-send "Mycroft" "Error opening application {application}. Do you have it installed? Was it spelled correctly whitelisted? Check ~/mycroft_launcher_error.txt for more details." -t 5000')
        else:
            run('notify-send "Mycroft" "I can\'t run that!"')
            self.speak_dialog("unknown_app")

    def open_repl(self, lang):
        """
        opens and voice interactive repl
        """
        self.acknowledge()
        term = self.settings.get("terminal")
        run(f"{term} -e {lang}")
            
    def stop(self):
        pass


def create_skill():
    return Launcher()

