# Cross-Platform Automated GUI Testing Framework

## Overview

This repository contains a demonstration video of a cross-platform automated GUI testing framework developed at Imagination Technologies. The framework successfully eliminated laborious manual GUI testing by providing comprehensive end-to-end automated testing of a debugger application, from the GUI interface through to the connected debug hardware.

<video width="320" height="240" controls>
  <source src="https://github.com/damienruscoe/GUITestExample/raw/refs/heads/master/gui_test_demo.ogv">
</video>

The video is located here: [video](https://github.com/damienruscoe/GUITestExample/raw/refs/heads/master/gui_test_demo.ogv)
The executed test script is located here: [test script](https://github.com/damienruscoe/GUITestExample/raw/refs/heads/master/gui_test_demo.ogv)

# TLDR;

## The Challenge

Manual GUI testing is time-consuming, error-prone, and requires significant QA resources. For complex debugger applications that interface with hardware, ensuring consistent behavior across platforms while maintaining test coverage is particularly challenging.

## The Solution

A custom-built, cross-platform GUI testing framework that enables automated end-to-end testing without requiring repeated manual intervention from the QA team. The framework operates significantly faster than human interaction, providing rapid feedback on application behavior.

## Architecture

The framework is built on a three-layer architecture:

### Layer 1: Core Primitives

Low-level operations for GUI interaction via a custom network protocol:

- **Element Navigation & Discovery**
  - Listing and navigating the tree of GUI elements
  - Searching and retrieving elements by type, name, or property
  - Waiting for elements to become visible

- **GUI Interactions**
  - Mouse clicks (left and right)
  - Keyboard input simulation
  - Element state queries (enabled/disabled, visible/hidden)

These primitives communicate with the System Under Test (SUT) through a custom network protocol, simulating user behavior by sending commands that drive the GUI programmatically.

### Layer 2: Utility Library

Higher-level abstractions built on core primitives:

- `click_main_menu_item()` - Navigate application menus
- `click_toolbar_item()` - Interact with toolbar elements
- Additional convenience functions for common UI patterns

### Layer 3: Domain-Specific API

Application-specific functionality providing intuitive test authoring:

- `create_hardware_breakpoint()` - Create breakpoints in the debugger
- `get_program_counter_value()` - Query hardware state
- `wait_for_device_connect()` - Synchronize with hardware connections
- Other domain-specific operations for debugger testing

## Video Demonstration

The included video demonstrates the framework in action, showing both the test setup interface and automated execution.

### Test Setup (Left Side of Video)

The test runner GUI provides manual test configuration:

1. **Test Suite Selection** - Choose from available test collections
2. **Test Selection** - Pick specific test to execute
3. **Hardware Selection** - Configure which debug hardware to connect to
4. **Test Execution** - Initiate the automated test run

### Automated Execution

Once initiated, the test executes completely autonomously. The video shows the `test_code_breakpoint_tupled_to_a_data_breakpoint_priming_a_data_breakpoint` test, which:

1. Waits for device connection
2. Loads a test program file (MIPS M5150 double loop)
3. Creates multiple hardware breakpoints (including temporary placeholders)
4. Establishes data watchpoint breakpoints
5. Removes temporary breakpoints
6. Configures breakpoint tupling and priming relationships
7. Executes the program until breakpoint hit
8. Verifies program counter location and memory values
9. Reports results back to the test runner

**Note:** The automated execution runs significantly faster than human operation, so individual actions may be difficult to follow in real-time.

### Example Test Code

```python
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
```

## Test Execution Flow

1. **Application Launch** - The debugger application starts and initializes
2. **Layout Configuration** - GUI layout is established for testing
3. **Breakpoint Creation** - Test-specific breakpoints are configured
4. **Resource Management** - Temporary breakpoints removed to free hardware resources
5. **Program Execution** - Target program runs until breakpoint condition met
6. **Verification** - Automated assertions validate:
   - Program counter location
   - Hardware memory values
   - Breakpoint behavior correctness
7. **Results Reporting** - Test outcomes displayed in runner and logged for CI/CD

## Deployment Options

The framework supports multiple execution modes:

- **GUI Test Runner** - Interactive test selection and execution (shown in video)
- **Command-Line Runner** - Headless execution for CI/CD pipelines with output to:
  - Standard output (stdout)
  - Log files
  - Database storage

## Key Benefits

- **Eliminates Manual Testing** - Removes need for repetitive QA manual testing
- **Cross-Platform** - Works consistently across different operating systems
- **End-to-End Coverage** - Tests complete stack from GUI to hardware
- **Rapid Execution** - Tests run faster than human operation
- **CI/CD Integration** - Supports automated pipeline integration
- **Regression Protection** - Catches issues before production

## Technical Highlights

- Custom network protocol for GUI automation
- Layered architecture enabling easy test authoring
- Hardware-in-the-loop testing capabilities
- Comprehensive assertion framework
- Flexible test execution and reporting

## Credits

This framework was designed and implemented entirely by the repository owner during their tenure at Imagination Technologies.
