from django.db.models import Q
from django.utils import timezone
import logging
from learning_paths.models import LearningPath, PathStep, UserPathProgress

from careers.models import Career, Skill, CareerSkill, LearningResource

logger = logging.getLogger(__name__)

def generate_learning_path(user, career, existing_skill_ids=None):
    """
    Generate a personalized learning path for a user based on their career goal
    and existing skills.
    
    Args:
        user: The User object for whom to generate a path
        career: The Career object representing the target career
        existing_skill_ids: List of skill IDs the user already possesses
        
    Returns:
        LearningPath: The created learning path object
    """
    if existing_skill_ids is None:
        existing_skill_ids = []
        
    logger.info(f"Generating learning path for user {user.username} for career: {career.name}")
    
    # Get all skills required for this career
    career_skills = CareerSkill.objects.filter(career=career)
    
    # Separate skills by importance
    essential_skills = [cs.skill for cs in career_skills.filter(importance='essential')]
    important_skills = [cs.skill for cs in career_skills.filter(importance='important')]
    useful_skills = [cs.skill for cs in career_skills.filter(importance='useful')]
    
    # Filter out skills the user already has
    essential_skills_to_learn = [s for s in essential_skills if s.id not in existing_skill_ids]
    important_skills_to_learn = [s for s in important_skills if s.id not in existing_skill_ids]
    useful_skills_to_learn = [s for s in useful_skills if s.id not in existing_skill_ids]
    
    # Create a learning path
    path_title = f"{career.name} Learning Path for {user.username}"
    path_description = f"Personalized learning path for {career.name} career, tailored to your experience level and existing skills."
    
    learning_path = LearningPath.objects.create(
        title=path_title,
        description=path_description,
        user=user,
        career=career,
        duration_weeks=estimate_duration(essential_skills_to_learn, important_skills_to_learn)
    )
    
    # Add the user to the path
    learning_path.users.add(user)
    
    # Add skills to the learning path
    all_skills_to_learn = essential_skills_to_learn + important_skills_to_learn + useful_skills_to_learn[:3]
    learning_path.skills.add(*all_skills_to_learn)
    
    # Create steps for the path
    create_steps_for_path(learning_path, essential_skills_to_learn, important_skills_to_learn, useful_skills_to_learn)
    
    return learning_path

def estimate_duration(essential_skills, important_skills):
    """
    Estimate the duration in weeks required to complete the learning path
    
    Args:
        essential_skills: List of essential skills to learn
        important_skills: List of important skills to learn
        
    Returns:
        int: Estimated number of weeks
    """
    # Simple estimation logic: 2 weeks per essential skill, 1 week per important skill
    essential_weeks = len(essential_skills) * 2
    important_weeks = len(important_skills)
    
    # Minimum duration is 1 week
    total_weeks = max(1, essential_weeks + important_weeks)
    
    # Cap at reasonable maximum (e.g., 26 weeks or 6 months)
    return min(total_weeks, 26)

def create_steps_for_path(learning_path, essential_skills, important_skills, useful_skills):
    """
    Create steps for a learning path based on the skills to learn
    
    Args:
        learning_path: LearningPath object to add steps to
        essential_skills: List of essential skills to learn
        important_skills: List of important skills to learn
        useful_skills: List of useful skills to learn
    """
    step_order = 1
    
    # Create steps for essential skills (highest priority)
    for skill in essential_skills:
        # Find best resources for this skill
        resources = get_resources_for_skill(skill)
        
        # Create skill learning step
        PathStep.objects.create(
            learning_path=learning_path,
            title=f"Learn {skill.name}",
            description=skill.description,
            step_type='skill',
            order=step_order,
            skill=skill,
            estimated_hours=20  # Default estimate
        )
        step_order += 1
        
        # Create resource steps for top resources
        for resource in resources[:2]:  # Limit to top 2 resources per skill
            PathStep.objects.create(
                learning_path=learning_path,
                title=f"Complete: {resource.title}",
                description=f"Resource for learning {skill.name}: {resource.description}",
                step_type='resource',
                order=step_order,
                skill=skill,
                resource=resource,
                estimated_hours=get_resource_hour_estimate(resource)
            )
            step_order += 1
    
    # Create steps for important skills (medium priority)
    for skill in important_skills:
        resources = get_resources_for_skill(skill)
        
        PathStep.objects.create(
            learning_path=learning_path,
            title=f"Learn {skill.name}",
            description=skill.description,
            step_type='skill',
            order=step_order,
            skill=skill,
            estimated_hours=15  # Default estimate
        )
        step_order += 1
        
        # Add just one resource for important skills
        if resources:
            PathStep.objects.create(
                learning_path=learning_path,
                title=f"Complete: {resources[0].title}",
                description=f"Resource for learning {skill.name}: {resources[0].description}",
                step_type='resource',
                order=step_order,
                skill=skill,
                resource=resources[0],
                estimated_hours=get_resource_hour_estimate(resources[0])
            )
            step_order += 1
    
    # Create steps for a few useful skills (lowest priority)
    for skill in useful_skills[:3]:  # Limit to top 3 useful skills
        PathStep.objects.create(
            learning_path=learning_path,
            title=f"Learn {skill.name}",
            description=skill.description,
            step_type='skill',
            order=step_order,
            skill=skill,
            estimated_hours=10  # Default estimate
        )
        step_order += 1
    
    # Add a final project or assessment step if there are enough skills
    if essential_skills or important_skills:
        PathStep.objects.create(
            learning_path=learning_path,
            title="Complete Capstone Project",
            description=f"Apply your {learning_path.career.name} skills by completing a portfolio project that demonstrates your abilities.",
            step_type='project',
            order=step_order,
            estimated_hours=40
        )

def get_resources_for_skill(skill):
    """
    Find the best learning resources for a skill
    
    Args:
        skill: Skill object to find resources for
        
    Returns:
        QuerySet: Learning resources sorted by relevance/rating
    """
    # Get resources directly linked to the skill
    resources = skill.resources.all()
    
    # If no resources found, try to find resources with similar names/descriptions
    if not resources:
        resources = LearningResource.objects.filter(
            Q(title__icontains=skill.name) | 
            Q(description__icontains=skill.name)
        )
    
    # Sort by rating (if available) and prioritize free resources
    return resources.order_by('-rating', '-is_free')

def get_resource_hour_estimate(resource):
    """
    Estimate the number of hours required to complete a resource
    
    Args:
        resource: LearningResource object
        
    Returns:
        int: Estimated hours
    """
    # Try to parse duration from the resource if available
    if resource.duration:
        if 'week' in resource.duration.lower():
            # Estimate 5 hours per week
            try:
                weeks = int(resource.duration.split()[0])
                return weeks * 5
            except (ValueError, IndexError):
                pass
        elif 'hour' in resource.duration.lower():
            try:
                hours = int(resource.duration.split()[0])
                return hours
            except (ValueError, IndexError):
                pass
    
    # Default estimates based on resource type
    if resource.resource_type == 'course':
        return 20
    elif resource.resource_type == 'book':
        return 15
    elif resource.resource_type == 'video':
        return 2
    elif resource.resource_type == 'article':
        return 1
    elif resource.resource_type == 'documentation':
        return 3
    else:
        return 5