```cpp
std::vector<int> primes{2, 3, 5, 7, 11};

primes.push_back(13);
primes.erase(primes.begin());
std::cout << primes[2] << '\n';
```
