<?php
// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve form data
    $name = $_POST['name'];
    $email = $_POST['email'];
    $phone = $_POST['phone'];
    $preferred_time = $_POST['preferred_time'];
    $remark = $_POST['remark'];
    
    // You can perform further validation or processing here
    
    // Redirect to thank you page
    header("Location: /thanku");
    exit; // Stop further execution of the script
}
?>
