#!/usr/bin/env just --working-directory .. --justfile
current-org := 'deepin-community'

# helper command for generating team metainfo yaml file for later modification
generate-team-metainfo-yml team-slug:
    cat .utils/team.gql | tr '\n' ' ' | xargs -I{file} gh api graphql --cache 5m --paginate -f team_slug='{{team-slug}}' -f login={{current-org}} -f query='{file}' > temp-result.txt
    # basic info
    echo -en "---\nname: {{team-slug}}\nblog:\nrss:\nproposal:\n  issue:\n  by:\n    handle:\n    id:\ndata-created: '-'\ndata-archived: '-'\nteam: {{team-slug}}\n" > {{team-slug}}.yml
    # repo (maintained)
    echo -en "repos:\n  maintained:\n" >> {{team-slug}}.yml
    cat temp-result.txt | jq -r '.data.organization.team.repositories.edges[] | select(.permission == "MAINTAIN") | "    - \(.node.name)"' >> {{team-slug}}.yml
    # repo (package)
    echo -en "  package:\n" >> {{team-slug}}.yml
    cat temp-result.txt | jq -r '.data.organization.team.repositories.edges[] | select(.permission == "WRITE") | "    - \(.node.name)"' >> {{team-slug}}.yml
    # members
    echo -en "members:\n" >> {{team-slug}}.yml
    cat temp-result.txt | jq -r '.data.organization.team.members.edges[].node | "  - handle: \(.login)\n    id: \(.databaseId)"' >> {{team-slug}}.yml
    rm temp-result.txt

# ensure team exists, if not, create one
ensure-team-exists team-yml:
    python3 .utils/team-management.py --action ensure_team_exists --organization {{current-org}} --file {{team-yml}}

# add/remove team member according to the provided team configuration yml file
update-team-member-n-repo team-yml: (ensure-team-exists team-yml)
    cat {{team-yml}} | yq '.team' | xargs -I{team-slug} gh api graphql --cache 5m --paginate -f team_slug='{team-slug}' -f login={{current-org}} -f query="$(cat .utils/team.gql)" > temp-result.txt
    # repo
    cat {{team-yml}} | yq '.repos.package' -o json > temp-repo-write-ref.json
    cat {{team-yml}} | yq '.repos.maintained' -o json > temp-repo-maintain-ref.json
    cat temp-result.txt | jq '.data.organization.team.repositories.edges[] | select(.permission == "MAINTAIN") | .node.name' | jq -s '.' > temp-repo-maintain-current.json
    cat temp-result.txt | jq '.data.organization.team.repositories.edges[] | select(.permission == "WRITE") | .node.name' | jq -s '.' > temp-repo-write-current.json
    cat {{team-yml}} | yq '.team' | xargs -I{team-slug} \
        python3 .utils/team-management.py --action team_repo_management \
                --ref temp-repo-maintain-ref.json \
                --cur temp-repo-maintain-current.json \
                --permission "maintain" \
                --organization {{current-org}} \
                --slug {team-slug}
    cat {{team-yml}} | yq '.team' | xargs -I{team-slug} \
        python3 .utils/team-management.py --action team_repo_management \
                --ref temp-repo-write-ref.json \
                --cur temp-repo-write-current.json \
                --permission "push" \
                --organization {{current-org}} \
                --slug {team-slug}
    # member
    cat {{team-yml}} | yq -r '.members' -o json > temp-member-ref.json
    cat temp-result.txt | jq '.data.organization.team.members.edges[].node | {handle: .login, id: .databaseId}' | jq -s '.' > temp-member-current.json
    cat {{team-yml}} | yq '.team' | xargs -I{team-slug} \
        python3 .utils/team-management.py --action team_member_management \
                --ref temp-member-ref.json \
                --cur temp-member-current.json \
                --organization {{current-org}} \
                --slug {team-slug}
