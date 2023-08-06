
FUNCTION_BLOCK process

    VAR_INPUT
        move_to_next_step : BOOL;
        fault_signal : BOOL;
    END_VAR

    VAR
        step_0 : BOOL := TRUE;
        step_1 : BOOL := FALSE;
        step_2 : BOOL := FALSE;
        step_3 : BOOL := FALSE;
        fault_occurred_in_step_1 : BOOL := FALSE;
    END_VAR

BEGIN

    // Record any fault that occurs during Step 1.
    IF step_1 AND fault_signal THEN
        fault_occurred_in_step_1 := TRUE;
    END_IF;

    // Step transitions (0 -> 1 -> 2 -> 3 -> 0).
    IF step_0 AND move_to_next_step THEN
        step_0 := FALSE;
        step_1 := TRUE;
    ELSIF step_1 AND move_to_next_step THEN
        step_1 := FALSE;
        step_2 := TRUE;
    ELSIF step_2 AND move_to_next_step THEN
        step_2 := FALSE;
        step_3 := TRUE;
        fault_occurred_in_step_1 := FALSE; // reset the "fault status"
    ELSIF step_3 AND move_to_next_step THEN
        step_3 := FALSE;
        step_0 := TRUE;
    END_IF;

END_FUNCTION_BLOCK
