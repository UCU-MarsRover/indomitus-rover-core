# Git Workflow and Branch Strategy

## Branch Structure

### Main Branches

- **`main`** - Stable, production-ready version of the rover
  - Only fully tested and approved code
  - Protected branch - no direct pushes allowed

- **`develop`** - Development integration branch
  - All feature branches are created from this branch
  - All completed features are merged back into this branch
  - Base branch for all team work

---

## Team Branch Naming Convention

### Branch Name Format

All team branches **must** follow this pattern:
```
{type}/{team}/{description}
```

### Branch Types

- `feature/` - New functionality
- `bugfix/` - Bug fixes
- `refactor/` - Code refactoring
- `experiment/` - Experimental features/tests
- `hotfix/` - Urgent fixes

### Team Names

- `arm` - Arm team
- `navigation` - Navigation team
- `science` - Science team
- `drone` - Drone team
- `suspension` - Suspension team





# PULL REQUEST TEMPLATE

```text
## Description
<!-- Provide a clear and concise description of what this PR does -->

## Type of Change
<!-- Mark the relevant option with an "x" -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test update
- [ ] Configuration change

## Changes Made
<!-- List the specific changes made in this PR -->

- 
- 
- 

## Testing (Future feature!!!)
<!-- Describe the tests you ran and how to reproduce them -->

- [ ] I have tested this locally
- [ ] All existing tests pass
- [ ] I have added new tests (if applicable)

### How to Test
<!-- Provide steps to test the changes -->

1. 
2. 
3. 

## Additional Notes
<!-- Any additional information that reviewers should know -->
```