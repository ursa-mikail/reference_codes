#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Global variables following the naming convention
int32_t global_int32_user_count = 0;
const char* constant_char_pointer_global_app_name = "FunctionCall Demo";

// Structure definition
typedef struct {
    int32_t int32_user_id;
    char char_array_username[50];
    double float64_user_balance;
} UserStructure_t;

// Function declarations following the naming convention
void Function__void__initialize_user_data(UserStructure_t* UserStructure_pointer_passed_in_user);
UserStructure_t* Function__UserStructure_pointer__create_new_user(const char* constant_char_pointer_passed_in_username, double float64_passed_in_initial_balance);
void Function__void__display_user_info(const UserStructure_t* constant_UserStructure_pointer_passed_in_user);
void Function__void__process_multiple_users();
double Function__double64__calculate_total_balance(const UserStructure_t* constant_UserStructure_pointer_passed_in_user1, const UserStructure_t* constant_UserStructure_pointer_passed_in_user2);
double Function__double64__calculate_interest(double float64_passed_in_principal, double float64_passed_in_rate, int32_t int32_passed_in_years);

int main() {
    printf("=== %s ===\n", constant_char_pointer_global_app_name);
    
    // Create a new user
    UserStructure_t* UserStructure_pointer_local_new_user = 
        Function__UserStructure_pointer__create_new_user("john_doe", 1000.50);
    
    if (UserStructure_pointer_local_new_user != NULL) {
        // Display user information
        Function__void__display_user_info(UserStructure_pointer_local_new_user);
        
        // Clean up
        free(UserStructure_pointer_local_new_user);
        UserStructure_pointer_local_new_user = NULL;
    }
    
    // Process multiple users
    Function__void__process_multiple_users();
    
    printf("Total users created: %d\n", global_int32_user_count);
    return 0;
}

// Function to initialize user data
void Function__void__initialize_user_data(UserStructure_t* UserStructure_pointer_passed_in_user) {
    if (UserStructure_pointer_passed_in_user == NULL) return;
    
    UserStructure_pointer_passed_in_user->int32_user_id = ++global_int32_user_count;
    UserStructure_pointer_passed_in_user->float64_user_balance = 0.0;
    memset(UserStructure_pointer_passed_in_user->char_array_username, 0, 
           sizeof(UserStructure_pointer_passed_in_user->char_array_username));
}

// Function to create a new user (calls another function)
UserStructure_t* Function__UserStructure_pointer__create_new_user(const char* constant_char_pointer_passed_in_username, 
                                       double float64_passed_in_initial_balance) {
    // Validate input
    if (constant_char_pointer_passed_in_username == NULL || 
        strlen(constant_char_pointer_passed_in_username) == 0) {
        printf("Error: Invalid username\n");
        return NULL;
    }
    
    // Allocate memory for new user
    UserStructure_t* UserStructure_pointer_local_new_user = 
        (UserStructure_t*)malloc(sizeof(UserStructure_t));
    
    if (UserStructure_pointer_local_new_user == NULL) {
        printf("Error: Memory allocation failed\n");
        return NULL;
    }
    
    // Call another function to initialize user data
    Function__void__initialize_user_data(UserStructure_pointer_local_new_user);
    
    // Set user-specific data
    strncpy(UserStructure_pointer_local_new_user->char_array_username, 
            constant_char_pointer_passed_in_username, 
            sizeof(UserStructure_pointer_local_new_user->char_array_username) - 1);
    UserStructure_pointer_local_new_user->char_array_username[49] = '\0'; // Ensure null termination
    UserStructure_pointer_local_new_user->float64_user_balance = 
        float64_passed_in_initial_balance;
    
    printf("User created successfully with ID: %d\n", 
           UserStructure_pointer_local_new_user->int32_user_id);
    
    return UserStructure_pointer_local_new_user;
}

// Function to display user information
void Function__void__display_user_info(const UserStructure_t* constant_UserStructure_pointer_passed_in_user) {
    if (constant_UserStructure_pointer_passed_in_user == NULL) {
        printf("Error: Cannot display null user\n");
        return;
    }
    
    printf("\n--- User Information ---\n");
    printf("User ID: %d\n", constant_UserStructure_pointer_passed_in_user->int32_user_id);
    printf("Username: %s\n", constant_UserStructure_pointer_passed_in_user->char_array_username);
    printf("Balance: $%.2f\n", constant_UserStructure_pointer_passed_in_user->float64_user_balance);
    printf("------------------------\n");
}

// Function that returns double64 - calculates total balance of two users
double Function__double64__calculate_total_balance(const UserStructure_t* constant_UserStructure_pointer_passed_in_user1, 
                                                  const UserStructure_t* constant_UserStructure_pointer_passed_in_user2) {
    double float64_local_total = 0.0;
    
    if (constant_UserStructure_pointer_passed_in_user1 != NULL) {
        float64_local_total += constant_UserStructure_pointer_passed_in_user1->float64_user_balance;
    }
    
    if (constant_UserStructure_pointer_passed_in_user2 != NULL) {
        float64_local_total += constant_UserStructure_pointer_passed_in_user2->float64_user_balance;
    }
    
    printf("Total balance calculated: $%.2f\n", float64_local_total);
    return float64_local_total;
}

// Function that returns double64 - calculates compound interest
double Function__double64__calculate_interest(double float64_passed_in_principal, 
                                             double float64_passed_in_rate, 
                                             int32_t int32_passed_in_years) {
    if (float64_passed_in_principal <= 0 || float64_passed_in_rate <= 0 || int32_passed_in_years <= 0) {
        printf("Error: Invalid input for interest calculation\n");
        return 0.0;
    }
    
    double float64_local_final_amount = float64_passed_in_principal;
    const double float64_local_rate_decimal = float64_passed_in_rate / 100.0;
    
    for (int32_t int32_local_i = 0; int32_local_i < int32_passed_in_years; int32_local_i++) {
        float64_local_final_amount *= (1.0 + float64_local_rate_decimal);
    }
    
    double float64_local_interest_earned = float64_local_final_amount - float64_passed_in_principal;
    
    printf("Interest calculation: Principal=$%.2f, Rate=%.2f%%, Years=%d -> Interest=$%.2f\n",
           float64_passed_in_principal, float64_passed_in_rate, int32_passed_in_years, float64_local_interest_earned);
    
    return float64_local_interest_earned;
}

// Additional function to demonstrate multiple users and function calls
void Function__void__process_multiple_users() {
    printf("\n=== Processing Multiple Users ===\n");
    
    // Local variables
    UserStructure_t* UserStructure_pointer_local_user1 = 
        Function__UserStructure_pointer__create_new_user("alice_smith", 2500.75);
    UserStructure_t* UserStructure_pointer_local_user2 = 
        Function__UserStructure_pointer__create_new_user("bob_johnson", 1800.25);
    
    // Constant local variable
    const int32_t constant_int32_local_max_users = 10;
    
    if (UserStructure_pointer_local_user1 != NULL) {
        Function__void__display_user_info(UserStructure_pointer_local_user1);
    }
    
    if (UserStructure_pointer_local_user2 != NULL) {
        Function__void__display_user_info(UserStructure_pointer_local_user2);
    }
    
    // Demonstrate double64 returning functions
    if (UserStructure_pointer_local_user1 != NULL && UserStructure_pointer_local_user2 != NULL) {
        double float64_local_total_balance = Function__double64__calculate_total_balance(
            UserStructure_pointer_local_user1, UserStructure_pointer_local_user2);
        
        printf("Combined wealth of both users: $%.2f\n", float64_local_total_balance);
        
        // Calculate interest on the total balance
        double float64_local_interest = Function__double64__calculate_interest(
            float64_local_total_balance, 5.0, 3); // 5% interest for 3 years
        
        printf("Potential interest earned over 3 years: $%.2f\n", float64_local_interest);
    }
    
    // Clean up
    if (UserStructure_pointer_local_user1 != NULL) {
        free(UserStructure_pointer_local_user1);
    }
    
    if (UserStructure_pointer_local_user2 != NULL) {
        free(UserStructure_pointer_local_user2);
    }
    
    printf("Maximum users allowed: %d\n", constant_int32_local_max_users);
}

/*
=== FunctionCall Demo ===
User created successfully with ID: 1

--- User Information ---
User ID: 1
Username: john_doe
Balance: $1000.50
------------------------

=== Processing Multiple Users ===
User created successfully with ID: 2
User created successfully with ID: 3

--- User Information ---
User ID: 2
Username: alice_smith
Balance: $2500.75
------------------------

--- User Information ---
User ID: 3
Username: bob_johnson
Balance: $1800.25
------------------------
Total balance calculated: $4301.00
Combined wealth of both users: $4301.00
Interest calculation: Principal=$4301.00, Rate=5.00%, Years=3 -> Interest=$677.95
Potential interest earned over 3 years: $677.95
Maximum users allowed: 10
Total users created: 3


=== Code Execution Successful ===
*/