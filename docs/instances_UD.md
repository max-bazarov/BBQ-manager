# Update and Delete instances

## Table of Contents

* [Short overview](#short-overview)
   * [No UD, only archivation](#no-ud-only-archivation)
      * [Exceptions:](#exceptions)
      * [Algorithm:](#algorithm)

## Short overview

This document describe how updates and deletions(UD further) should be managed in this project. This part of documentation is appliable to next models:

MasterProcedure, Material.

## No UD, only archivation

We cannot update or delete instances of this models as it affects historic data, this is anacceptable in our case. So, we must archive this 
instances and create new in order to prevent historic data damaging.

### Exceptions:

- MasterProcedure: deletable only if it is not linked to any other instances.
- Material: deletable only if it is not linked to any other instances.

### Algorithm:

1. Request for UD operation.
2. Mark initial inctance as archived
3. [For update only] create new instance with updated information
