"""
SCAG LIVE TV
AI NEWS DIRECTOR
"""


class NewsDirector:

    def create_plan(
        self,
        analysis,
        scene="auto",
        headline="",
        lower_third="",
        ticker=""
    ):

        if scene == "auto":

            if analysis.get(
                "orientation"
            ) == "portrait":

                selected_scene = "standing"

            else:

                selected_scene = "main"

        else:

            selected_scene = scene

        return {

            "scene":
                selected_scene,

            "headline":
                headline,

            "lower_third":
                lower_third,

            "ticker":
                ticker,

            "layout":
                "automatic",

            "preserve_presenter":
                True,

            "preserve_movement":
                True,

            "preserve_voice":
                True,

            "preserve_expression":
                True,

            "preserve_clothing":
                True,

            "camera_adaptation":
                True,

            "automatic_graphics":
                True

        }
