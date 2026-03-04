function hello($n){
write-host "Hello "+$n
return $null}

function add($a,$b){
$x=$a+$b
return $x
}

$result=add 3 5
hello "world"
write-host $result
