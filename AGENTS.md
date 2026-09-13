# Repository editing policy

The GitHub profile `README.md` is locked as an append-only profile artifact.

## Allowed change

Only add new project information inside the existing `# Projects` section, before `## Engineering principles`.

## Forbidden changes

Do not delete, rewrite, reorder, reformat, shorten, expand, or otherwise modify any existing line in `README.md`.

Do not update profile, biography, current-focus, engineering-principles, technology-landscape, research/collaboration, footer, existing project descriptions, existing project links, or existing repository-table rows unless the repository owner explicitly revokes this lock.

For a new project, insert a new project block or an additional project entry while preserving all pre-existing README content byte-for-byte.

The CI workflow `.github/workflows/profile-content-lock.yml` enforces this rule for README changes.
