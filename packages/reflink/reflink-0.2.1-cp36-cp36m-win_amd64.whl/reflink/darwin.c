#include <AvailabilityMacros.h>
/* NOTE: sys/clonefile.h is available since OS X 10.12 */
#if MAC_OS_X_VERSION_MIN_REQUIRED >= MAC_OS_X_VERSION_10_12
#include <sys/clonefile.h> /* for clonefile(2) */
#include <errno.h>

int reflink_clone_file(char *oldpath, char *newpath) {
    int rc;
    rc = clonefile(oldpath, newpath, 0);
    if (rc == 0) return 0;
    if (errno == ENOTSUP) {
        return -4;
    }
    return rc;
}
#else
int reflink_clone_file(char *oldpath, char *newpath) {
    return -4;
}
#endif
