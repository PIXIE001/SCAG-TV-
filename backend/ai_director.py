"""
SCAG LIVE TV
AI NEWS DIRECTOR
"""


class AIDirector:

    def choose_scene(
        self,
        analysis,
        requested_scene="auto"
    ):

        if requested_scene != "auto":

            return requested_scene


        if analysis.sitting:

            return "main"


        return "standing"


    def choose_presenter_layout(
        self,
        people
    ):

        if people >= 2:

            return "two_presenter"

        return "single_presenter"


    def create_plan(
        self,
        analysis,
        headline="",
        lower_third="",
        ticker=""
    ):

        scene = self.choose_scene(
            analysis
        )


        layout = (
            self.choose_presenter_layout(
                analysis.people
            )
        )


        return {

            "scene":
                scene,

            "layout":
                layout,

            "headline":
                headline,

            "lower_third":
                lower_third,

            "ticker":
                ticker,

            "preserve_original_voice":
                True,

            "preserve_original_movement":
                True,

            "preserve_original_expression":
                True,

            "preserve_original_clothing":
                True

        }
