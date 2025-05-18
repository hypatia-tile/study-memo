# Unit testing from functional approach

Yes, it is possible to improve **expressiveness** in Java by using **records** and **lambda expressions**, and here's how:

---

### 1. **Records**  
Records were introduced in Java 14 (preview) and standardized in Java 16. They provide a concise way to define immutable data carriers.

**Before (Verbose):**
```java
public class User {
    private final String name;
    private final int age;

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String name() { return name; }
    public int age() { return age; }
}
```

**With Record (Concise and Expressive):**
```java
public record User(String name, int age) {}
```

**Why it’s more expressive:**  
- Reduces boilerplate  
- Clearly conveys intent: "This class is just data"

---

### 2. **Lambda Expressions**  
Introduced in Java 8, lambdas enable functional-style programming with less code.

**Before (Anonymous Class):**
```java
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};
```

**With Lambda:**
```java
Runnable r = () -> System.out.println("Hello");
```

**Why it’s more expressive:**  
- Focuses on the *what*, not the *how*  
- Improves readability, especially for functional interfaces (like `Predicate`, `Function`, `Consumer`)

---

### Combined Use Example:
```java
record Command(String name, Runnable action) {}

public class Main {
    public static void main(String[] args) {
        Command greet = new Command("greet", () -> System.out.println("Hi!"));
        greet.action().run();  // Outputs: Hi!
    }
}
```

This pattern is especially useful in clean architecture, event-driven systems, and when designing APIs.

Would you like to see how this pattern could help with DTOs or functional pipelines?

## NOTE2

Yes, **records can be nested** in Java—meaning you can define a record *inside* another class or even inside another record. This lets you build more expressive, structured data models, which is useful for simulating concepts like `Either` or `Monad` patterns, even though Java isn’t inherently a functional language like Haskell.

Let’s walk through an **analogy** and a **code-based example** for an `Either`-like monad using nested records and functional interfaces.

---

### **Analogy: Nested Boxes and Actions**

Think of a `record` as a **box** that holds a value, and a **lambda** as an **action** you can apply to what's inside the box.

An `Either<L, R>` is like a **two-way locker**: one side might hold a *left* value (like an error), the other a *right* value (like a successful result). You want to write code that says:

> "If there's a right value, do this with it; otherwise, keep the left."

---

### **Java Example: Nested Record-Based `Either`**

```java
import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        Either<String, Integer> result = new Either.Right<>(42);
        
        Either<String, Integer> mapped = result.map(x -> x + 1);
        mapped.ifRight(System.out::println); // prints 43
    }

    public sealed interface Either<L, R> permits Either.Left, Either.Right {
        <U> Either<L, U> map(Function<? super R, ? extends U> mapper);

        void ifRight(java.util.function.Consumer<? super R> consumer);

        record Left<L, R>(L value) implements Either<L, R> {
            public <U> Either<L, U> map(Function<? super R, ? extends U> mapper) {
                return new Left<>(value);
            }

            public void ifRight(java.util.function.Consumer<? super R> consumer) {
                // do nothing
            }
        }

        record Right<L, R>(R value) implements Either<L, R> {
            public <U> Either<L, U> map(Function<? super R, ? extends U> mapper) {
                return new Right<>(mapper.apply(value));
            }

            public void ifRight(java.util.function.Consumer<? super R> consumer) {
                consumer.accept(value);
            }
        }
    }
}
```

---

### **Why This Works**
- `sealed` + `record` lets you define an ADT-style structure.
- `map()` is a functional interface that applies the transformation if you're on the `Right` side.
- The nested `Left` and `Right` records are clear and concise, mimicking the functional `Either` structure.

Would you like to add flatMap support to make it monadic in full?

## NOTE3

Great! You **can use `record` and functional interfaces to make unit tests more expressive and structured**—especially when you're trying to represent **test cases as data** and **assertions as lambdas**. Here's how you can combine them effectively:

---

## ✅ Goal: Use `record` + functional interfaces in Unit Tests

### 💡 Use Case 1: Representing Test Cases with Records

Define a record to hold test case data (input, expected output, etc.):

```java
public record TestCase<I, O>(I input, O expected, java.util.function.Function<I, O> function) {}
```

Then in your test:

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class MyFunctionTest {
    @Test
    public void testCases() {
        var test1 = new TestCase<>(
            5,
            25,
            x -> x * x
        );

        var test2 = new TestCase<>(
            3,
            9,
            x -> x * x
        );

        runTest(test1);
        runTest(test2);
    }

    private <I, O> void runTest(TestCase<I, O> testCase) {
        O actual = testCase.function().apply(testCase.input());
        assertEquals(testCase.expected(), actual);
    }
}
```

---

### 💡 Use Case 2: Composing Test Logic with Functional Interfaces

You can even define an interface for your own test logic:

```java
@FunctionalInterface
public interface Assertion<I> {
    void check(I input);
}
```

Then define your tests like this:

```java
public record LogicTest<I>(I input, Assertion<I> assertion) {}

@Test
public void testAssertions() {
    LogicTest<Integer> test = new LogicTest<>(
        10,
        x -> assertEquals(100, x * x)
    );
    test.assertion().check(test.input());
}
```

---

## 🧠 Benefits
- Clear, declarative test cases (like a test DSL).
- Supports dynamic, parameterized testing.
- Makes it easy to refactor and group related logic.

---

Would you like a JUnit 5 version using `@ParameterizedTest` with records and `Stream`?

## NOTE5

Perfect. If you want to **formally define the notions of** `Input`, `RetMock`, and `Expected`, a clean way in Java is to create a structured `record` that captures the core idea of a test case.

Let’s define this in the context of unit testing, where:

- `Input` – is the input to the function under test.
- `RetMock` – is the return value mocked or the behavior stubbed out (if you're mocking dependencies).
- `Expected` – is the expected result (what the system under test should return).

---

## ✅ Step-by-Step: Define a Reusable TestCase Record

```java
import java.util.function.Function;

public record TestCase<I, M, E>(
    I input,                      // actual input
    M retMock,                    // mocked return (e.g., return of a mock service)
    E expected,                   // expected output
    Function<I, E> function       // function under test
) {}
```

---

## ✅ Example with Unit Test (Using JUnit 5)

Suppose you're testing a function that multiplies a number and adds a mocked value:

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class LogicTest {

    Function<Integer, Integer> testLogic(int retMock) {
        return input -> input * 2 + retMock;
    }

    @Test
    public void runTestCases() {
        var case1 = new TestCase<>(
            3,                  // input
            4,                  // retMock (e.g., mocked external service returns 4)
            10,                 // expected: 3*2 + 4 = 10
            testLogic(4)        // function with "mocked" behavior
        );

        var case2 = new TestCase<>(
            5,
            1,
            11,
            testLogic(1)
        );

        run(case1);
        run(case2);
    }

    private <I, M, E> void run(TestCase<I, M, E> testCase) {
        E actual = testCase.function().apply(testCase.input());
        assertEquals(testCase.expected(), actual);
    }
}
```

---

## 🧠 Why This Pattern Works

- The `record` cleanly separates **input**, **mocked data**, and **expected result**.
- It keeps your tests **DRY** and scalable.
- You can **easily refactor** to test multiple edge cases just by changing the input data.

---

Would you like to extend this with **mocking frameworks** (like Mockito) for real service dependencies?

## NOTE6

Excellent—when doing **matrix-style testing** (a.k.a. **Cartesian product testing**), it's common to define `Input` as a **record of multiple lists**, especially when you're testing a function across combinations of multiple dimensions like `List<A>, List<B>, List<C>`.

You can represent this clearly using **nested records** and a general-purpose `TestCase` structure.

---

## ✅ Step 1: Define the Input Record

```java
public record Input<A, B, C>(List<A> listA, List<B> listB, List<C> listC) {}
```

This encapsulates the triple of test parameters cleanly.

---

## ✅ Step 2: Define the Full Test Case

```java
import java.util.function.Function;

public record MatrixTestCase<A, B, C, M, E>(
    Input<A, B, C> input,        // structured input
    M retMock,                   // mocked behavior if applicable
    E expected,                  // expected output/result
    Function<Input<A, B, C>, E> function // function under test
) {}
```

---

## ✅ Step 3: Use It in a Unit Test

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

public class MatrixTest {

    @Test
    void runMatrixTest() {
        // input: 1 value in each list
        Input<Integer, String, Double> input =
            new Input<>(List.of(2), List.of("x"), List.of(1.5));

        // mocked value (optional, here null)
        Integer retMock = null;

        // expected output
        String expected = "2-x-1.5";

        // function under test
        Function<Input<Integer, String, Double>, String> func = in -> {
            return in.listA().get(0) + "-" + in.listB().get(0) + "-" + in.listC().get(0);
        };

        MatrixTestCase<Integer, String, Double, Integer, String> testCase =
            new MatrixTestCase<>(input, retMock, expected, func);

        run(testCase);
    }

    private <A, B, C, M, E> void run(MatrixTestCase<A, B, C, M, E> testCase) {
        E actual = testCase.function().apply(testCase.input());
        assertEquals(testCase.expected(), actual);
    }
}
```

---

## 🧠 Why This Is Powerful

- Supports highly **parameterized tests** with explicit structure.
- Encourages **pure function testing**.
- Allows **mocking** without needing Mockito, if you inject behavior via functional interfaces.
- Promotes **readability** and **maintainability**.

---

Would you like a generator function that produces the **full Cartesian product** of `List<A>`, `List<B>`, and `List<C>` as inputs?