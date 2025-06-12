Cases if we have required and nullable:

 1. A property is required and can't be null
    It must appear in the dictionary and must have a valid value
 2. A property is required and can be null
    It must appear in the dictionary, but it can have a null value
 3. A property is optional and can't be null
    It may appear in the dictionary and can't be null if provided
 4. a property is optional and can be null
    It may appear in the dictionary and can be either a valid value or null if provided

What I think is important:

 - On create: required properties must have a valid value in the object. optional
   can appear in the object and can be null (same effect as not being in the object)
 - On update: required properties may be in the object and if they are they must be
   valid. optional may be if the object with a valid value or null (to clear the
   field)
