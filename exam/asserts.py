irrelevant = object()


class ChangeWatcher(object):

    def __init__(self, thing, *args, **kwargs):
        self.thing = thing
        self.args = args
        self.kwargs = kwargs
        self.expected_before = kwargs.pop('before', irrelevant)
        self.expected_after = kwargs.pop('after', irrelevant)

    def __enter__(self):
        self.before = self.__apply()

        if not self.expected_before is irrelevant:
            check = self.before == self.expected_before
            assert check, self.__precondition_failure_msg_for('before')

    def __exit__(self, type, value, traceback):
        self.after = self.__apply()

        if not self.expected_after is irrelevant:
            check = self.after == self.expected_after
            assert check, self.__precondition_failure_msg_for('after')

        assert self.before != self.after, self.__equality_failure_message

    def __apply(self):
        return self.thing(*self.args, **self.kwargs)

    @property
    def __equality_failure_message(self):
        return 'Expected before %s != %s after' % (self.before, self.after)

    def __precondition_failure_msg_for(self, condition):
        return '%s value did not change (%s)' % (
            condition,
            getattr(self, condition)
        )


class AssertsMixin(object):
    assertChanges = ChangeWatcher
