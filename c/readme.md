

## Variable Naming Convention
```
Pattern: <type>_<if_is_pointer>_<if_is_constant | structure>_<passed_in | global | local>_<name>

Components:
<type> - Data type with size specification

<if_is_pointer> - Pointer indicator

<if_is_constant | structure> - Constant or structure indicator

<passed_in | global | local> - Scope specification

<name> - Descriptive name
```

Examples:

```
// Basic types with scope
int32_global_user_count
double_local_temp_value
char_local_initial

// Pointers
UserStructure_pointer_local_new_user
char_pointer_passed_in_username

// Constants
constant_int32_local_max_users
constant_char_pointer_global_app_name

// Arrays
char_array_local_buffer
int32_array_passed_in_data
```

### Detailed Breakdown:
#### Type Specifications:
```
int32 - 32-bit integer

double or float64 - 64-bit floating point

char - character

UserStructure - custom structure type

bool - boolean
```
#### Pointer Indicators:
```
pointer - indicates the variable is a pointer

(omitted) - indicates the variable is not a pointer
```
####  Constant/Structure Indicators:
```
constant - indicates the variable is const

Structure - indicates a structure type

(omitted) - regular variable
```
#### Scope Indicators:
```
global - global variable

local - local variable

passed_in - function parameter
```

---
## Function Naming Convention
```
Pattern: Function__<if_is_pointer>_<return_type>__<name>
Components:
Function - Mandatory function prefix

<if_is_pointer>_<return_type> - Return type specification

<name> - Descriptive function name
```	

Examples:
```
// Void return types
Function__void__initialize_user_data
Function__void__display_user_info
Function__void__process_multiple_users

// Pointer return types
Function__UserStructure_pointer__create_new_user
Function__char_pointer__get_username

// Value return types
Function__double64__calculate_total_balance
Function__double64__calculate_interest
Function__int32__get_user_count
Function__bool__is_valid_user
```


### Detailed Breakdown:
#### Return Type Specifications:
```
void - no return value

int32 - returns 32-bit integer

double64 - returns 64-bit double

bool - returns boolean

UserStructure_pointer - returns pointer to UserStructure

char_pointer - returns char pointer
```

### Benefits of These Conventions
1. Type Safety

```
// Immediately clear what types are involved
double float64_local_interest = Function__double64__calculate_interest(1000, 5, 3);
UserStructure_t* UserStructure_pointer_local_user = Function__UserStructure_pointer__create_new_user(...);
```

2. Scope Clarity

```
// Know the variable scope at a glance
int32_global_user_count        // Global - be careful with modifications
double_local_temp_value        // Local - safe to modify
char_pointer_passed_in_name    // Parameter - don't free unless documented
```

3. Memory Management

```
// Clear ownership responsibilities
UserStructure_pointer_local_user = Function__UserStructure_pointer__create_new_user(...);
// ^ This returns a pointer that MUST be freed later

constant_UserStructure_pointer_passed_in_user
// ^ This is a const parameter - DON'T free or modify
```

4. Self-Documenting Code

```
// The names tell the whole story
Function__double64__calculate_compound_interest(
    double float64_passed_in_principal,
    double float64_passed_in_rate,
    int32_t int32_passed_in_years)
```

5. Error Prevention

```
// Prevents common C errors:
constant_char_pointer_passed_in_filename  // Can't modify this
UserStructure_pointer_local_data          // Must check for NULL and free
```


### Work Examples

1. Variable Declaration

```
// Good - follows convention
int32_local_count = 0;
UserStructure_pointer_local_user = NULL;
constant_char_pointer_global_app_name = "MyApp";

// Avoid - ambiguous
int count;
User* user;
const char* app_name;
```

2. Function Definitions

```
// Good - clear return type and purpose
double Function__double64__calculate_area(double float64_passed_in_radius) {
    return 3.14159 * float64_passed_in_radius * float64_passed_in_radius;
}

// Avoid - ambiguous return type
double calculate_area(double radius) {
    return 3.14159 * radius * radius;
}
```

3. Structure Usage
```
// Clear structure variable naming
UserStructure_t UserStructure_local_temp_user;
UserStructure_t* UserStructure_pointer_local_dynamic_user;

// Structure members also follow clear naming
typedef struct {
    int32_user_id;
    char_array_username[50];
    double float64_balance;
} UserStructure_t;
```

4. Pointer Management
```
// Clear pointer lifecycle
UserStructure_t* UserStructure_pointer_local_user = 
    Function__UserStructure_pointer__create_new_user(...);
    
if (UserStructure_pointer_local_user != NULL) {
    Function__void__use_user(UserStructure_pointer_local_user);
    free(UserStructure_pointer_local_user);
    UserStructure_pointer_local_user = NULL;
}
```

### Common Patterns
1. Function Calling Another Function

```
UserStructure_t* Function__UserStructure_pointer__create_new_user(...) {
    UserStructure_t* UserStructure_pointer_local_user = malloc(...);
    Function__void__initialize_user_data(UserStructure_pointer_local_user);
    return UserStructure_pointer_local_user;
}
```

2. Error Handling

```
bool Function__bool__validate_input(constant_char_pointer_passed_in_input) {
    if (constant_char_pointer_passed_in_input == NULL) {
        return false;
    }
    return true;
}
```

3. Memory Allocation

```
UserStructure_t* Function__UserStructure_pointer__allocate_user() {
    UserStructure_t* UserStructure_pointer_local_user = 
        (UserStructure_t*)malloc(sizeof(UserStructure_t));
    if (UserStructure_pointer_local_user == NULL) {
        return NULL;
    }
    return UserStructure_pointer_local_user;
}
```

### Tooling Benefits
1. Easy Searching

```
Search "Function__double64__" to find all double-returning functions
Search "_global_" to find all global variables
Search "_pointer_" to find all pointer variables
```

2. Code Completion
```
Type "Function__" to see all functions
Type "int32_" to see all integer variables
Type "_local_" to see all local variables
```

3. Refactoring

```
Changing return type from pointer to value:
Function__UserStructure_pointer__create_user → Function__UserStructure__create_user
```

Refer: [example.c](example.c)


## Key Features of the Updated Convention:
### Consistent Function Naming Pattern:
```c
Function__void__initialize_user_data()                    // Returns void
Function__UserStructure_pointer__create_new_user()        // Returns UserStructure pointer
Function__void__display_user_info()                       // Returns void
Function__double64__calculate_total_balance()            // Returns double
Function__double64__calculate_interest()                 // Returns double
```

### Benefits of the Double Underscore Convention:

1. Clear Return Type Identification
```c
// Immediate understanding of what the function returns:
Function__void__display_user_info()              // Returns nothing
Function__double64__calculate_interest()         // Returns a double
Function__UserStructure_pointer__create_new_user() // Returns a UserStructure pointer
```

2. Easy Function Discovery
```c
// All functions start with "Function__" making them easy to find
// Grouped by return type when sorted alphabetically:
Function__double64__calculate_interest
Function__double64__calculate_total_balance
Function__UserStructure_pointer__create_new_user
Function__void__display_user_info
Function__void__initialize_user_data
Function__void__process_multiple_users
```

3. Self-Documenting Code
```c
// The function name tells you everything:
Function__double64__calculate_total_balance(user1, user2)
// - It's a function
// - Returns double64
// - Calculates total balance
// - Takes two user parameters
```

4. Compile-Time Safety
```c
// Clear expectations about return types:
double float64_local_interest = Function__double64__calculate_interest(1000, 5, 3);
// The naming convention reminds you that this returns a double

UserStructure_t* UserStructure_pointer_local_user = Function__UserStructure_pointer__create_new_user(...);
// Clearly returns a pointer that needs memory management
```

5. Enhanced Code Readability
```c
// When reading code, function purposes are crystal clear:
int main() {
    // Function calls are self-explanatory
    UserStructure_t* UserStructure_pointer_local_user = Function__UserStructure_pointer__create_new_user(...);
    Function__void__display_user_info(UserStructure_pointer_local_user);
    
    double float64_local_total = Function__double64__calculate_total_balance(user1, user2);
    double float64_local_interest = Function__double64__calculate_interest(float64_local_total, 5.0, 3);
}
```

### Conclusion
These conventions provide:
```
Immediate understanding of variable types and scopes

Clear function signatures and return types

Reduced cognitive load when reading code

Better error prevention through explicit naming

Improved team collaboration with consistent patterns
```




