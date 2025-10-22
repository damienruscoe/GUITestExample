
@test
def test_code_breakpoint_tupled_to_a_data_breakpoint_priming_a_data_breakpoint():
    """ Data --- Primed by ---> Data --- tupled to ---> Code """
    application.wait_for_device_connect()
    application.load_program_file(mips_m5150_double_loop.path)
    breakpoint_region = create_test_layout4()
    target_tree = get_target_tree()

    create_hardware_breakpoint('0x80000000') # temporary
    create_hardware_breakpoint('0x80000008') # temporary

    create_hardware_breakpoint(test_store_instruction_inside_loop) # Code hw resource 6
    _create_test_data_watch_breakpoint('&test1', '5') # Data hw resource 2
    _create_test_data_watch_breakpoint('&test', '10') # Data hw resource 3

    delete_breakpoint(breakpoint_region, '0x80000000') # Remove temporary
    delete_breakpoint(breakpoint_region, '0x80000008') # Remove temporary

    add_tuple_to_data_breakpoint(breakpoint_region, '&test', re.compile(test_store_instruction_inside_loop + '.*'))
    add_primed_to_data_breakpoint(breakpoint_region, '&test1', re.compile('&test.*'))

    run_until_hardware_breakpoint(target_tree)

    assertPCAtExpression('%s + 4' % test_1_store_instruction_inside_loop)
    assertExpressionValuesEqual({'test':       '10',
                                 'test1':      '5'})

