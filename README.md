# endpoint-backend-coding-challenge

To run this, simply run
> python directories.py \[\<optional file path\>\]

# Constraints
I noticed a couple things while looking over the email, and I figured I'd write out the constraints and assumptions I have here.
* How the input was supposed to be collected was left "underspecified". I decided with that I'd accept two consumers, stdin one by one
* Display of filepath is not specified for order (alphabetical, date added, a theordical date modified)
* Do we allow batch creation/deletion? For this I decided no, but it would be a product question worth researching for your users.
* I used sys and enum from the standard library, I assume this is okay as it's not an external helper library.
* Move is not explictly stated to be unable to move files that aren't there.
* Assuming delete can ripple delete- as the example for "DELETE foods/fruits/apples" allows deletion even though fuji is never explicitly deleted
* In retrospec, create is not defined like this either. Will assume we don't auto create folders.
* Can we delete a folder that contains subfolders? For this exercise I will assume not, but ya know.

# Some things I learned (skill issues)
* Used enums wrong. Took 10 minutes to figure out. Pepehands.
* Aparently when initializing my variables it was using leftover child object which lead my to an infinately deep recursive route?
    * Still not sure why that happened, maybe there is a critique in here for how I was using default values in the object constructor
    * Caleb of like 30 minutes later, turns out when you give a default param, that function keeps the same memory address for that, and will then cause self reference. Code was switched to explicit declaration.