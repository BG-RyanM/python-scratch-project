async def do_some_stuff_for_me():
    with trace.transaction("do_some_stuff_for_me", "function"): # Should I use some name besides "function"?

        with trace.span("do_setup"):
            # Do various setup

        with trace.span("do_my_big_loop"):
            while(keep_doing_the_loop):
                with trace.span("task_A_in_loop"):
                    # Do task A stuff

                with trace.span("task_B_in_loop"):
                    # Do task B stuff

                with trace.span("task_C_in_loop"):
                    # Do task C stuff
                    if need_to_do_special_subtask:
                        # This subtask is only run sometimes
                        with trace.span("subtask_C1"):
                            # Do the subtask

container_dict = yield container_db.find_one({"barcode": barcode}, sort=[("created_time", DESCENDING)])