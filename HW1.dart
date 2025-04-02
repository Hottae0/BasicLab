import 'dart:io';

void main(List<String> arguments) async {
  int num = int.parse(stdin.readLineSync()!);

  int sum = 0;

  while(num > 0){
    sum += num % 10;
    num = num ~/ 10;
  }

  sum += num;

  print(sum);

}


