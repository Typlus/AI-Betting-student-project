from pathlib import Path

class SkillManager:
    def __init__(self, skills_directory="skills"):
        self.skills_directory = Path(skills_directory)

    def load_skill(self,skill_name):
        """
        load skills instruction from markdown file
        """

        skill_path = self.skills_directory / skill_name / "skill.md"

        if not skill_path.exists():
            raise FileNotFoundError( f"Skill '{skill_name} was not found.")

        return skill_path.read_text(encoding="utf-8")

    