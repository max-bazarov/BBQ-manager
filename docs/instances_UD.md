# Update and Delete instances

## Short overview

This document describe how updates and deletions(UD further) should be managed in this project. This part of documentation is appliable to next models:

MasterProcedure, Material.

## No UD, only archivation

We cannot update or delete instances of this models as it affects historic data, this is anacceptable in our case. So, we must archive this 
instances and create new in order to prevent historic data damaging.

Algorithm:

1. Request for UD operation.
2. Mark initial inctance as archived
3. [For update only] create new instance with updated information
