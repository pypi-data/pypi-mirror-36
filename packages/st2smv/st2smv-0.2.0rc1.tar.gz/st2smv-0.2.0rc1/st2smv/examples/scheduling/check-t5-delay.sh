
st2smv --check-schedule \
    --input schedule-t5.json state-t5-delay.json \
    --metadata metadata.json \
    --output-directory results-t5_delay \
    --verbosity debug \
    --solver-path SynthSMV \
;
