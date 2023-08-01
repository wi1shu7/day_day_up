<?php
    ini_set('session.save_path', dirname(__FILE__).'\session_save');
    session_start();
    var_dump($_SESSION);