from adapt.intent import IntentBuilder 
from mycroft import MycroftSkill, intent_handler
from os import system as run
from subprocess import Popen, PIPE
from sys import stdout


class Launcher(MycroftSkill):

    def __init__(self):
        super().__init__()
        #self.initialize()
        #self.apps = self.settings
        
    def initialize(self):
        self.register_entity_file("app.entity")
        #self.register_intent_file("launch.intent", self.handle_launch_intent)
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
        #run(f'notify-send "app_title" "{app_title}"')
        app_name = self.equivilency(app_title.lower())
        #run(f'notify-send "app name" "{app_name}"')
        white_list = self.settings.get("white list").split(",")
        #run(f'notify-send "white list" "{white_list}"')
        if app_name in self.settings.keys():
            run(f'notify-send "debug" "{app_name} in seting.keys()"')
            return self.settings.get(app_name)
        #elif app_title not in white_list and app_title not in self.settings.keys():
        #    return 1
        elif (app_title in white_list) or (app_name in white_list):
            return app_name
        else:
            return 1
        
    @intent_handler("launch.intent")
    def handle_launch_intent(self, app):
        #run(f'notify-send "DEBUG" "{app.data.get("app")}"')
        self.acknowledge()
        application = self.get_target_app(app.data.get("app")) # self.settings.get(self.equivilency(app.data.get("app")))
        #self.acknowledge()
        #run(f'notify-send "DEBUG" "{self.settings.get("REPLs")}"')
        repls = self.dict_reader(self.settings.get("REPLs"))
        if application in repls.keys():
            self.open_repl(application)
        elif application != 1:
            run(f'notify-send "Running" "{application}"')
            try:
                run(application)
            except:
                self.speak("bru... I can't do that.")
                run(f'echo "got error when running :  {app.__dict__}\nsettings :  {type(self.settings)}\nsettings :  {self.settings}" > ~/mycroft_launcher_error.txt')
                run(f'notify-send "Mycroft" "Error opening application {application}. Do you have it installed? Was it spelled correctly whitelisted? Check ~/mycroft_launcher_error.txt for more details." -t 5000')
        else:
            run('notify-send "Mycroft" "I can\'t run that!"')
            self.speak_dialog("unknown_app")

    def dict_reader(self, text):
        aliases = {}
        for pair in text.split(","):
            name, value = pair.split("=")
            aliases[name.strip()] = value if value.strip() != "" else name.strip()
        return aliases
            
    def open_repl_legacy(self, lang):
        """
        opens and voice interactive repl
        """
        #self.acknowledge()
        run('notify-send "mycroft" "runing repl"')
        term = self.settings.get("terminal")
        run(f"{term} -e {lang}")

    def open_repl(self, lang):
        run(f'notify-send "debug" "open repl called"')
        term = self.settings.get("terminal")
        p = Popen(term + " -e " + lang, shell=True, stderr=PIPE)
        n = 0
        while True:
            run(f'notify-send "debug" "inside while loop"')
            out = p.stderr.read(1)
            if (out == '' and p.poll() != None) or (type(out) == bytes):
                break
            if out != '':
                self.say
                stdout.write(str(n) + str(out))
                stdout.flush()
            n += 1
            
    def stop(self):
        pass


def create_skill():
    return Launcher()
