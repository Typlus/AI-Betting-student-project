from agent.skill_manager import SkillManager

def main():
    manager = SkillManager()

    skill = manager.load_skill("Statistic_Analysis")
    print("\n--- LOADED SKILL ---")
    print(skill)

if __name__ == "__main__":
    main()
