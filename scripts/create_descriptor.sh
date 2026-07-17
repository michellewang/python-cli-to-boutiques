#!/usr/bin/env bash
set -euo pipefail

# -- Create dump file --
if [[ "$PARSER_TYPE" == "click" ]]; then
  CLICK_ARGS=(--output "$DUMP_FILE")
  if [[ -n "$CLICK_PROG_NAME" ]]; then
    CLICK_ARGS+=(--prog "$CLICK_PROG_NAME")
  fi
  if [[ -n "$CLICK_PARENT_LOCATION" ]]; then
    CLICK_ARGS+=(--parent "$CLICK_PARENT_LOCATION")
  fi
  python ./scripts/run_clickdump.py "${CLICK_ARGS[@]}" "$PARSER_LOCATION"
elif [[ "$PARSER_TYPE" == "argparse" ]]; then
  python ./scripts/run_argdump.py --output "$DUMP_FILE" "$PARSER_LOCATION"
else
  echo "Error: PARSER_TYPE must be 'argparse' or 'click', got '$PARSER_TYPE'" >&2
  exit 1
fi
cat "$DUMP_FILE"

# -- Build Boutiques descriptor --
npx -y --package @styx-api/cli styx build "$DUMP_FILE" --out styx-out --backend boutiques

# -- Move to output path --
mkdir -p "$(dirname "$OUTPUT_PATH")"
mv ./styx-out/boutiques/descriptor.json "$OUTPUT_PATH"

# -- Apply updates --
UPDATES_DESCRIPTOR_ARGS=()
if [[ "${EXCLUDE_VERSION}" == "true" ]]; then
  UPDATES_DESCRIPTOR_ARGS+=(--remove-version)
fi
if [[ -n "${UPDATES_FILE}" ]]; then
  UPDATES_DESCRIPTOR_ARGS+=(--updates-file "$UPDATES_FILE")
fi
if [[ -n "${UPDATES_STR}" ]]; then
  UPDATES_DESCRIPTOR_ARGS+=(--updates-str "${UPDATES_STR}")
fi
if [[ "${#UPDATES_DESCRIPTOR_ARGS[@]}" -gt 0 ]]; then
  python ./scripts/update_descriptor.py --descriptor "$OUTPUT_PATH" "${UPDATES_DESCRIPTOR_ARGS[@]}"
fi

# -- Print final descriptor --
cat "$OUTPUT_PATH"
