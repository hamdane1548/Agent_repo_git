from etl import createUser, AiAgent_RepoSelect


def invokeagent(profiles,jobDescriptoin,TechStack):
    user = createUser(profiles)
    github_with_repo = AiAgent_RepoSelect(jobDescriptoin=jobDescriptoin, tech=TechStack, profile=user)
    return github_with_repo