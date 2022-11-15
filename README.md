# Dual_EC_DRBG lab

## 1

Let **[&middot;]<sub>x</sub>** be a function returning the x-coordinate of a point on a (Weierstrass) elliptic curve **E**.<br>
Let **lift_x(.)** be a function taking as argument an x-coordinate of a point and returns all the possible points with this x-coordinate.<br>
Let **P<sub>x</sub>** be an x-coordinate ant let **S = lift_x(P<sub>x</sub>)** be the set of points having **P<sub>x</sub>** as x-coordinate.

We show the following statement :

#### For any constant **l &in; &Zopf;<sup>*</sup>**, if **0 &notin; S**, then for all **Q &in; S, [lQ]<sub>x</sub>** is the same.

**S** can contain 0, 1 or 2 points.

If **|S| = 0** or **|S| = 1**, the statement is trivially true.

For the case **|S| = 2**, we prove the statement by induction :

### Base step : case l = 1

we want to show that :

#### For **Q<sub>1</sub> &in; S, Q<sub>2</sub> &in; S</sub>**: **[1Q<sub>1</sub>]<sub>x</sub> = [1Q<sub>2</sub>]<sub>x</sub>**

By definition of **S**, we have **[Q<sub>1</sub>]<sub>x</sub> = [Q<sub>2</sub>]<sub>x</sub>**

Now, **Q<sub>1</sub> = 1Q<sub>1</sub>** and **Q<sub>2</sub> = 1Q<sub>2</sub>**

Thus, we have **[1Q<sub>1</sub>]<sub>x</sub> = [1Q<sub>2</sub>]<sub>x</sub>**

### Induction step

We want to show that :

#### For **Q<sub>1</sub> &in; S, Q<sub>2</sub> &in; S</sub>** : if **[iQ<sub>1</sub>]<sub>x</sub> = [iQ<sub>2</sub>]<sub>x</sub>** is true for all **i &in; [1, l]**, then **[(l+1) Q<sub>1</sub>]<sub>x</sub> = [(l+1) Q<sub>2</sub>]<sub>x</sub>**

To prove this, we are going to use

- The point addition formula
- The fact that for all **R<sub>1</sub>, R<sub>2</sub> &in; E** with **R<sub>1</sub> &ne; R<sub>2</sub>**: **[R<sub>1</sub>]<sub>x</sub> = [R<sub>2</sub>]<sub>x</sub> => [R<sub>1</sub>]<sub>y</sub> = -[R<sub>2</sub>]<sub>y</sub>**
  - This is true because if **R<sub>1</sub> = (x, y<sub>1</sub>)** satisfies the elliptic curve formula (i.e. **y<sub>1</sub><sup>2</sup> = x<sup>3</sup> + ax + b**), then the only other **y** such that **y<sup>2</sup> = x<sup>3</sup> + ax + b** is **-y<sub>1</sub>**.

We have :

**[(l+1) Q<sub>1</sub>]<sub>x</sub> = [l Q<sub>1</sub> + Q<sub>1</sub>]<sub>x</sub>**

(we use the point adition formula)

**= ([l Q<sub>1</sub>]<sub>y</sub> - [Q<sub>1</sub>]<sub>y</sub>)<sup>2</sup> / ([l Q<sub>1</sub>]<sub>x</sub> - [Q<sub>1</sub>]<sub>x</sub>)<sup>2</sup> - [l Q<sub>1</sub>]<sub>x</sub> - [Q<sub>1</sub>]<sub>x</sub>**

(we use the fact that **[Q<sub>1</sub>]<sub>x</sub> = [Q<sub>2</sub>]<sub>x</sub>** and **[lQ<sub>1</sub>]<sub>x</sub> = [lQ<sub>2</sub>]<sub>x</sub>**)

**= ([l Q<sub>1</sub>]<sub>y</sub> - [Q<sub>1</sub>]<sub>y</sub>)<sup>2</sup> / ([l Q<sub>2</sub>]<sub>x</sub> - [Q<sub>2</sub>]<sub>x</sub>)<sup>2</sup> - [l Q<sub>2</sub>]<sub>x</sub> - [Q<sub>2</sub>]<sub>x</sub>**

**= (-[l Q<sub>1</sub>]<sub>y</sub> + [Q<sub>1</sub>]<sub>y</sub>)<sup>2</sup> / ([l Q<sub>2</sub>]<sub>x</sub> - [Q<sub>2</sub>]<sub>x</sub>)<sup>2</sup> - [l Q<sub>2</sub>]<sub>x</sub> - [Q<sub>2</sub>]<sub>x</sub>**

(we use the fact that **[Q<sub>1</sub>]<sub>y</sub> = - [Q<sub>2</sub>]<sub>y</sub>** and **[l Q<sub>1</sub>]<sub>y</sub> = - [l Q<sub>2</sub>]<sub>y</sub>**)

**= ([l Q<sub>2</sub>]<sub>y</sub> - [Q<sub>2</sub>]<sub>y</sub>)<sup>2</sup> / ([l Q<sub>2</sub>]<sub>x</sub> - [Q<sub>2</sub>]<sub>x</sub>)<sup>2</sup> - [l Q<sub>2</sub>]<sub>x</sub> - [Q<sub>2</sub>]<sub>x</sub>**

(we use the point addition formula)

**= [l Q<sub>2</sub> + Q<sub>2</sub>]<sub>x</sub> = [(l+1) Q<sub>2</sub>]<sub>x</sub>**

## 2

- We work in the elliptic curve [P-256](https://neuromancer.sk/std/nist/P-256)
- **P** and **Q** are points on the elliptic curve
- **n** is the order of the elliptic curve

## 3

In this attack, we are going to recover **state2** from **output1** and **output2**.

To do this, we start from **output1** and we go upward in the diagram by applying the inverse of the operations. We end up with several candidate values for **state2**. We then find the right one by generating the corresponding outputs and comparing them to **output2**.

Once **state2** is known, we use it to generate the subsequent outputs.

The code for this attack is implemented in the function `clone_dual_ec2_drbg` of the file `dualec_attack.py`.

### Step 1 : truncation bruteforce

To reverse the **>> 8** operation, we have to perform a bruteforce as we do not know what the truncated bits are. This gives 2<sup>8</sup> candidates.

### Step 2 : lift_x

To reverse the **[·]<sub>x</sub>** operation, we use **lift_x**, which can return 0, 1 or 2 points.

- If 0 points are returned, no candidates are added to the result of this step. 
- If 1 point is returned, it is added as a candidate. 
- If 2 points are returned, they are the opposite of each other. Only the first one is added as a candidate

As a lot of the x value candidates from step 1 do not correspond to a point on the curve, the number of candidates is reduced.

We end up with several candidates, one of which is the correct value for **state1 * Q** or the opposite of **state1 * Q**.

### Step 3 : from **state1 * Q** to **state1 * P**

Let **inv_d** be the inverse of **d** modulo **n**.

Now, as **n** is the order of the elliptic curve, for all **m &in; &Nopf;** we have **m P** = **(m mod n) P**.

Thus, we have **inv_d * state1 * Q = state1 * inv_d * d *  P = state1 * P**

By the statement that we have proven in part 1, we know that if we multiply the opposite of **state1 * Q** by **inv_d** we get the opposite of **state1 * P**

Therefore, we multiply each candidate from step 2 by **inv_d** and as a result we get several candidates, one of which is the correct value for **state1 * P** or the opposite of **state1 * P**.

### Step 4 : find state1 candidates

We apply **[·]<sub>x</sub>** to each candidate from step 3. We know that one of the resulting values is the correct value for **step1**.

### Step 5 : find the right state1

For each **step1** candidate, we apply the operation **[· Q]x >> 8**. This gives us the output of the PRNG if the candidate was the state. Among the candidates, the right **step1** is the one that corresponds to **output2**.

### Clone the PRNG

Now that we know **state2**, we create an instance of the PRNG and set its state to **state2**. This means our PRNG is in the same state as the original PRNG was after having outputted **output2**.

The outputs generated by calling the `next` method of our new PRNG are equal to **output3**, **output4**, ... of the original PRNG.

## 4

We write the function `discrete_logarithm` in the file `dualec_attack.py`. This function is based on the [baby step giant step algorithm](https://en.wikipedia.org/wiki/Baby-step_giant-step).

