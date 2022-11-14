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
  - This is true because if **R<sub>1</sub> = (x, y<sub>1</sub>)** satisfies the elliptic curve formula (i.e. **y<sub>1</sub><sup>2</sup> = x<sup>3</sup> + ax + b**), then the only other y such that **y<sup>2</sup> = x<sup>3</sup> + ax + b** is **-y<sub>1</sub>**.

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

