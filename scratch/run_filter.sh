
#!/bin/bash
export FILTER_BRANCH_SQUELCH_WARNING=1

git filter-branch --env-filter '
    while read commit date; do
        if [ "$GIT_COMMIT" = "$commit" ]; then
            export GIT_AUTHOR_DATE="$date"
            export GIT_COMMITTER_DATE="$date"
        fi
    done < "C:/Users/notic/OneDrive/Desktop/LLM/NanoLLM/scratch/date_map.txt"
' -f HEAD
