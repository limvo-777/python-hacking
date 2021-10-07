<?php
$_ip=$_GET['ip'];
system("ping -c 4 ".$_ip);
?>