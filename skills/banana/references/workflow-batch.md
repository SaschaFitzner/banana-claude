# Workflow: Batch Variations

> Generate N variations of an idea, or run a CSV-driven batch of distinct images.
>
> **Prerequisites:** If not already loaded, read `references/gemini-models.md` and `references/prompt-engineering.md` before Step 2.

## Batch Pipeline

1. **Estimate cost first** — ALWAYS show cost estimate before running any batch (see Cost Estimate below)
2. **Construct base brief** — Follow `references/workflow-generate.md` Steps 1-4 to build the Reasoning Brief for the core idea
3. **Generate variations** — Create N distinct prompts by rotating one component per generation (see Variations Strategy)
4. **Execute sequentially** — Call `generate.py` N times with distinct prompts; log each result
5. **Present results** — Show all output paths with a brief description of what varies in each

## Variations Strategy

For `/banana batch <idea> [N]` (default N=3), rotate ONE component per variation. Rotating multiple components simultaneously makes results uncontrollable and impossible to compare.

| Variation | Component to rotate | Example |
|-----------|--------------------|---------|
| 1 | Lighting | golden hour → blue hour → overcast diffused |
| 2 | Composition | tight close-up → medium shot → wide establishing |
| 3 | Style | photorealistic → illustrated → minimal flat vector |
| 4+ | Continue rotating: Perspective, Color grade, Subject age/demographic, Time period | — |

ALWAYS keep Subject, Action, and Context identical across all variations.

## CSV Batch

For larger batches with distinct concepts per row:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/batch.py --csv path/to/file.csv
```
The script outputs a generation plan with cost estimates. Before executing, review the plan:
- Check estimated cost against user's budget
- Flag any prompt that may trigger `IMAGE_SAFETY`
- Confirm all rows have distinct subjects

Then execute each row via `generate.py`. See `references/cost-tracking.md` for per-image pricing.

## Cost Estimate

ALWAYS run before executing a batch:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py estimate \
  --model gemini-3.1-flash-image-preview \
  --resolution 2K \
  --count N
```
Show the estimate to the user and wait for confirmation before proceeding.

## Log After Batch

After all images are generated, log the session:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log \
  --model gemini-3.1-flash-image-preview --resolution 2K --prompt "batch: [idea summary]"
```
