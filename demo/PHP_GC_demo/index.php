<?php
    highlight_file(__FILE__);
    class AA{
        public $a;
        public $aa;
        public function __destruct(){
            echo $this->a;
        }
        
        public function __toString(){
            return "hello";
        }
    }
    
    class BB{
        public $b;
        public function __toString(){
            ($this -> b)();
            return "6";
        }
        public function good($c){
            eval($c);
        }
    }
    
    class CC{
        public $c;
        public $cc;
        public function __invoke(){
            ($this->c)($this->cc);
        }
        public function __toString(){
            return "ok,but wrong";
        }
        public function __call($ccc, $cccc){
            call_user_func($ccc,$cccc);
        }
    }
	var_dump($_GET);
    $a = unserialize($_GET['QAQ_O.o']);
    throw new Error("NoNoNo!Hacker!");
