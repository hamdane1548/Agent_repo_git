from pydantic import BaseModel, Field
from typing import List


class ScoreBreakdown(BaseModel):
    technology_match: int = Field(
        ge=0, le=25,
        description="Match between repository technologies and job technologies. Max 25."
    )

    architecture_software_engineering: int = Field(
        ge=0, le=20,
        description="Architecture and software engineering quality. Max 20."
    )

    job_responsibility_match: int = Field(
        ge=0, le=20,
        description="How well the repository demonstrates job responsibilities. Max 20."
    )

    relevant_technical_features: int = Field(
        ge=0, le=15,
        description="Relevant APIs, security, databases, AI, messaging, cloud, DevOps, etc. Max 15."
    )

    code_quality: int = Field(
        ge=0, le=10,
        description="Code quality, organization, maintainability and engineering practices. Max 10."
    )

    testing_ci_cd_devops: int = Field(
        ge=0, le=5,
        description="Testing, CI/CD, Docker and DevOps practices. Max 5."
    )

    documentation: int = Field(
        ge=0, le=5,
        description="README and project documentation quality. Max 5."
    )


class InterviewQuestion(BaseModel):
    question: str = Field(
        description="Technical interview question based on the repository and job."
    )

    topic: str = Field(
        description="Topic of the question, for example Architecture, Security, API, Database, etc."
    )


class RepositoryEvaluation(BaseModel):
    repository_name: str = Field(
        description="Name of the candidate repository."
    )

    match_score: int = Field(
        ge=0,
        le=100,
        description="Overall repository relevance score for the job, from 0 to 100."
    )

    match_level: str = Field(
        description="Excellent Match, Strong Match, Good Match, Partial Match, Weak Match or Very Weak Match."
    )

    project_summary: str = Field(
        description="Concise summary of the repository."
    )

    architecture: str = Field(
        description="Description of the project's architecture and main components."
    )

    technologies: List[str] = Field(
        description="Technologies, frameworks, libraries, databases and infrastructure identified in the repository."
    )

    job_requirements_matched: List[str] = Field(
        description="Job requirements demonstrated by this repository."
    )

    missing_requirements: List[str] = Field(
        description="Important job requirements not demonstrated or weakly demonstrated."
    )

    evidence: List[str] = Field(
        description="Evidence from files or folders supporting the evaluation."
    )

    inspected_files: List[str] = Field(
        max_length=2,
        description="Maximum 2 source-code files inspected in detail."
    )

    engineering_evaluation: str = Field(
        description="Evaluation of the candidate's software engineering practices."
    )

    score_breakdown: ScoreBreakdown = Field(
        description="Detailed scoring breakdown."
    )

    interview_questions: List[InterviewQuestion] = Field(
        min_length=7,
        max_length=8,
        description="7 to 8 technical interview questions based on this repository and the job."
    )


class RepositoryRanking(BaseModel):
    repository_name: str
    score: int = Field(ge=0, le=100)


class CandidateRepositoryAnalysis(BaseModel):
    repositories: List[RepositoryEvaluation] = Field(
        description="Evaluation of every candidate repository."
    )

    ranking: List[RepositoryRanking] = Field(
        description="Repositories ranked from highest to lowest match score."
    )

    best_repository: str = Field(
        description="Repository with the highest job relevance."
    )

    best_repository_reason: str = Field(
        description="Why this repository is the strongest match."
    )

    overall_recommendation: str = Field(
        description="Strongly Relevant, Relevant, Potentially Relevant, Weakly Relevant or Not Relevant."
    )