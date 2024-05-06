<?php
include '../connect.php';
  if(isset($_POST['submit'])) {
      $cart_items = $_POST['item'];
      $order_id = $_POST['order_id'];
      $stmt = $connection->prepare("INSERT INTO tblorder_items (item, order_id) VALUES (?, ?)");

  if (!$stmt) {
    $error = "Database error: " . $connection->error;
  } else {

    $stmt->bind_param("ss", $cart_items, $order_id);
    $result = $stmt->execute();

  if (!$result) {
    $error = "Query execution error: " . $stmt->error;
  } else {
    header("Location: ../includes/home.php");
    exit();
  }
  }
  $stmt->close();
}
?>
<!DOCTYPE html>

<html>
    <head>
    <meta charset="UTF-8">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <!-- FONT LINK GIKAN GOGOL AND ICONS ATA -->
    <link rel = "stylesheet" href = "https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@48,400,0,0">
    <script src = "../js/script.js"></script>
    <link rel="stylesheet" href="../css/jewelry.css">
    <title>Login and Register</title>
    </head>
<body>
<div class="container">
    <h1>Jewelry Section</h1>
    <div class="jewelry-item">
      <div class="item-details">
        <a href = "../dashboard.php"><img src="../images/jewelry1.jpg" alt="Jewelry 1" aria-label="Gold Necklace"></a>
        <a href = "../checkout.php"><h2>Gold Necklace</h2></a>
        <p>Beautiful gold necklace with intricate design.</p>
      </div>
      <div class="item-details">
      <a href = "../checkout.php"><img src="../images/jewelry2.webp" alt="Jewelry 2" aria-label="Silver Bracelet"></a>
      <a href = "../checkout.php"><h2>Silver Bracelet</h2></a>
        <p>Elegant silver bracelet with sparkling diamonds.</p>
      </div>
      <div class="item-details">
      <a href = "../checkout.php"><img src="../images/jewelry3.jpg" alt="Jewelry 3" aria-label="Diamond Ring"></a>
      <a href = "../checkout.php"><h2>Diamond Ring</h2></a>
        <p>Exquisite diamond ring for special occasions.</p>
      </div>
    </div>
  </div>
</body>
</html>