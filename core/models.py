from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.core.urlresolvers import reverse
#from social_auth.models import UserSocialAuth
#import facepy
#import json
from social_auth.signals import pre_update, socialauth_registered
from social_auth.backends.facebook import FacebookBackend
import datetime


class BrewerManager(UserManager):  # or use BaseUserManager if I can def create_(super)user funcs
    pass


class Brewer(AbstractUser):
    """ New in Dj 1.5: https://docs.djangoproject.com/en/dev/topics/auth/#auth-custom-user """
    objects = BrewerManager()

    ### profile
    #proficiencies = [('newbie', 'First Timer'),
                #        ('novice', 'Novice'),
            #            ('intermediate', 'Intermediate'),
         #               ('expert', 'Expert'),
          #              ('brewmaster', 'Brewmaster'),
            #        ]
    #bio = models.TextField(null=False, blank=True)
    #age = models.IntegerField(null=False, blank=True, default=21)
    birthday = models.DateField(null=True)
    age = models.IntegerField(null=True)
    #proficiency = models.CharField(blank=False, null=False, choices=proficiencies, max_length=50)

    # quasi- permissions
    show_facebook = models.BooleanField(default=False)
    show_email = models.BooleanField(default=False)

    # signal handlers related to this model
    def _facebook_extra_values(sender, user, response, details, **kwargs):
        birthday = response.get('birthday')  # response.get('birthday')
        user.birthday = datetime.datetime.strptime(birthday, '%m/%d/%Y')
        user.age = int((datetime.datetime.now() - user.birthday).days / 365.2425)
        user.save()
        return True
    pre_update.connect(_facebook_extra_values, sender=FacebookBackend)

    def _new_user_handler(sender, user, response, details, **kwargs):
        #user.age = response.get('birthday')
        return True
    socialauth_registered.connect(_new_user_handler, sender=None)

    ### attributes
    # contributed_cash is the amount of money contributed
    # outstanding_fees are fees that have not yet been paid or charged against deposit
    contributed_cash = models.FloatField(null=False, blank=False, default=0.0)
    outstanding_fees = models.FloatField(null=False, blank=False, default=0.0)

    ### reverse relationships
    # equipment contributed
    # equipment borrowed
    # vouchers offered & active

    ### properties
    def _has_outstanding_fees(self):
        """ A member can only borrow when they owe no late charges """
        if self.outstanding_fees > 0:
            return True
        return False
    has_outstanding_fees = property(_has_outstanding_fees)

    def _contributed_equipment_value(self):
        """ Cash value of contributed equipment """
        return 44.4  # FIXME
    contributed_equipment_value = property(_contributed_equipment_value)

    def _contributed_equipment_and_cash_value(self):
        """ Cash value of contributed equipment and cash deposits """
        return self.contributed_cash + self.contributed_equipment_value
    deposit = property(_contributed_equipment_and_cash_value)

    def _sum_of_vouchers(self):
        """ Cash value of committed vouchers currently outstanding """
        return 33.2  # FIXME
    sum_of_vouchers = property(_sum_of_vouchers)

    def _accrued_primary_late_charges(self):
        """ Cash value of late charges accrued against PRIMARY active loans """
        return 12  # FIXME
    accrued_primary_late_charges = property(_accrued_primary_late_charges)

    def _accrued_secondary_late_charges(self):
        """ Cash value of late charges accrued against SECONDARY active loans """
        return 11  # FIXME
    accrued_secondary_late_charges = property(_accrued_secondary_late_charges)

    def _available_deposit(self):
        ret = self.deposit \
            - self.sum_of_vouchers \
            - self.accrued_primary_late_charges \
            - self.accrued_secondary_late_charges
        return ret
    available_deposit = property(_available_deposit)

    def _active_days_delinquent(self):
        """" Number of days deliquent on outstanding, active equipment loans """
        return 0  # FIXME
    active_days_delinquent = property(_active_days_delinquent)

    def _historical_days_delinquent(self):
        """ Number of days delinquent on all active and inactive equipment loans """
        return 0  # FIXME
    historical_days_delinquent = property(_historical_days_delinquent)

    def _full_name(self):
        if self.first_name or self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return ""
    full_name = property(_full_name)

    def __unicode__(self):
        if self.full_name:
            return self.full_name
        return self.username

    def _username_link(self):
        return "<a href=\"%s\">%s</a>" % (reverse('brewer-profile', args=[str(self.id)]), self.__unicode__())
    username_link = property(_username_link)

    def _profile_link(self):
        return "<a href=\"%s\">View Profile</a>" % reverse('brewer-profile', args=[str(self.id)])
    profile_link = property(_profile_link)

    def _facebook_uid(self):
        if not self.show_facebook:
            return None

        facebook_uid = None
        try:
            facebook_uid = self.social_auth.filter(provider='facebook').get().uid
        except:
            pass
        return facebook_uid
    facebook_uid = property(_facebook_uid)

    def _facebook_link(self):
        fbid = self.facebook_uid
        if fbid:
            return """
            <a href="https://www.facebook.com/%s" target="_blank">Facebook Brewer</a>
            """ % fbid
        return ""
    facebook_link = property(_facebook_link)

    def _facebook_link_inline(self):
        fbid = self.facebook_uid
        if fbid:
            return """
            [<a href="https://www.facebook.com/%s" target="_blank">FB</a>]
            """ % fbid
        return ""
    facebook_link_inline = property(_facebook_link_inline)

    def _email_link(self):
        if self.show_email:
            return """
            <a href="mailto:%s" target="_blank">Email Brewer</a>
            """ % self.email
        return ""
    email_link = property(_email_link)

    def _email_link_inline(self):
        if self.show_email:
            return """
            [<a href="mailto:%s" target="_blank">@</a>]
            """ % self.email
        return ""
    email_link_inline = property(_email_link_inline)

    def _equipment_count(self):
        return self.equipment_set.filter(contributed=False).count()
    equipment_count = property(_equipment_count)


#class LibraryBranch(models.Model):
    # e.g. Toad Lane
    #name = models.CharField(null=False, blank=False, max_length=50)


class Commodity(models.Model):
    # e.g. 5 gallon glass car boy
    # the reserve ratio is the % portion of the value that must be deposited in order to borrow
    name = models.CharField(null=False, blank=False, max_length=50)
    description = models.TextField(null=False, blank=False)
    value = models.IntegerField(null=False, blank=False, verbose_name='Replacement cost')
    #total_quantity_wanted = models.IntegerField(null=False, default=0, blank=False)
    #rental_period_in_days = models.IntegerField(default=30)
    #late_charge_per_day = models.FloatField(null=False, default=1, blank=False)
    #reserve_requirement = models.FloatField(null=False, default=1.0, blank=False, help_text='This is the ratio of deposits:cost before granting a tool loan')
    #request_expiration_period_in_days = models.IntegerField(default=7)

    ### reverse relationships
    # stock listing
    # reservations
    def _quantity_owned(self):
        return self.equipment_set.filter(contributed=True).count()
    quantity_owned = property(_quantity_owned)

    def _quantity_available(self):
        return self.equipment_set.filter(contributed=True, loan=None).count()
    quantity_available = property(_quantity_available)

    def _quantity_waiting_list(self):
        return self.loan_set.filter(commodity=self, equipment=None).count()
    quantity_waiting_list = property(_quantity_waiting_list)

    def _quantity_wanted(self):
        return self.total_quantity_wanted - self.quantity_owned
    quantity_wanted = property(_quantity_wanted)

    def _quantity_p2p_total(self):
        return self.equipment_set.filter(contributed=False).count()  # FIXME: add filter for checked out!
    quantity_p2p_total = property(_quantity_p2p_total)

    def _quantity_p2p_available(self):
        return self.equipment_set.filter(contributed=False, p2p_is_checked_out=False).count()
    quantity_p2p_available = property(_quantity_p2p_available)

    def _availability_string(self):
        return "[Branch: %i/%i available] [P2P: %i/%i available]" % (self.quantity_available,
            self.quantity_owned, self.quantity_p2p_available, self.quantity_p2p_total)
    availability_string = property(_availability_string)

    def __unicode__(self):
        return self.name


class EquipmentOffer(models.Model):
    # e.g. Patrick wants to deposit his 5 gallon car boy
    owner = models.ForeignKey('core.Brewer', null=False, blank=False)
    tool = models.CharField(null=False, blank=False, max_length=50)
    description = models.TextField(null=False, blank=True, help_text="(Optional) Please share any additional information here.")
    value = models.FloatField(null=False, blank=False, verbose_name="Estimated value", help_text="Please estimate the replacement cost for this tool.")


class EquipmentManager(models.Manager):
    def branch_set(self):
        return self.filter(contributed=True)

    def p2p_set(self):
        return self.filter(contributed=False)


class Equipment(models.Model):
    objects = EquipmentManager()
    # e.g. Patrick's contributed 5 gallon car boy
    contributor = models.ForeignKey('core.Brewer', null=False, blank=False)  # FIXME: rename to owner?
    commodity = models.ForeignKey('core.Commodity', null=False, blank=False)
    label = models.CharField(null=True, blank=False, max_length=30, help_text="Enter a short label to help you remember which tool this is")
    description = models.TextField(null=False, blank=True, help_text="(Optional) You may wish to record any details about the tool here")
    #shared = models.BooleanField(null=False, default=False, help_text="Do you wish to offer this tool for others to borrow?")
    contributed = models.BooleanField(null=False, default=False)
    p2p_is_checked_out = models.BooleanField(default=True)  # default to checked out /Private use
    #location = models.ForeignKey('core.LibraryBranch', null=False, blank=False)

    def _status(self):
        if self.contributed:
            try:
                loan = Loan.objects.get(equipment=self)
                return "Loaned to <a href=%s>%s" % (reverse('brewer-profile', kwargs={'pk': loan.borrower.id}), loan.borrower.username)
            except:
                return "Available Branch"
        else:
            if self.p2p_is_checked_out:
                return "Unavailable"
            else:
                return "Available P2P"
    status = property(_status)


class Loan(models.Model):
    # e.g. Jerry would like to borrow a 5 gallon car boy
    # e.g. Jerry borrowed a 5 gallon car boy
    # Has three stages: Reservation, Active Loan, Inactive
    # ...which can be discerned by accessing these datetime fields
    #   Reservation:    data_requested
    #   Active:     data_requested, date_borrowed
    #   Inactive:   data_requested, date_borrowed, date_returned

    ### attributes
    borrower = models.ForeignKey('core.Brewer', null=False, blank=False)

    ### "Loan Reservation" attributes
    commodity = models.ForeignKey('core.Commodity', null=False)
    date_requested = models.DateField(auto_now_add=True)
    earnest_deposit = models.FloatField(null=False, blank=False, default=0.0)

    ### "Loan Reservation" properties
    def _is_reservation(self):
        return not self.date_borrowed
    is_reservation = property(_is_reservation)

    def _is_covered(self):
        """ Boolean: Is there enough personal and vouched deposits to cover the rental? """
        return False  # FIXME
    is_covered = property(_is_covered)

    def _amount_covered(self):
        """ Returns sum of deposits currently allocated to this rental reservation """
        return 0.0  # FIXME
    amount_covered = property(_amount_covered)

    def _amount_not_covered(self):
        """ Returns amount of deposits still needed to fulfill this equipment loan """
        return 10.0  # FIXME
    amount_not_covered = property(_amount_not_covered)

    def _is_reservation_expired(self):
        """ Boolean: Has the rental reservation expired? """
        return False  # FIXME

    ### "Loan" attributes
    equipment = models.OneToOneField('core.Equipment', null=True, blank=True)
    age_verified = models.BooleanField(null=False, default=False, blank=False)
    date_borrowed = models.DateField(null=True, blank=True)
    date_returned = models.DateField(null=True, blank=True)

    ### "Loan" properties
    def _is_active(self):
        return False  # FIXME
    is_active = property(_is_active)

    def _is_overdue(self):
        return False  # FIXME
    is_overdue = property(_is_overdue)

    def _accrued_late_charges(self):
        return 0.0  # FIXME
    accrued_late_charges = property(_accrued_late_charges)

    def _is_underwater(self):
        return False  # FIXME
    is_underwater = property(_is_underwater)

    ### string for use in django admin
    def __str__(self):
        return str(self.borrower) + " (requested " + str(self.date_requested) + ")"


class Voucher(models.Model):
    # e.g. Alice is willing to help Jerry out by vouching $5 toward his deposit requirement
    # Brewers also use a Voucher object when providing their own collateral ... KISS
    underwriter = models.ForeignKey('core.Brewer', null=False, blank=False)
    loan = models.ForeignKey('core.Loan', null=False, blank=False)
    amount = models.FloatField(null=False, blank=False)
    date_offered = models.DateField(auto_now_add=True)


class Transaction(models.Model):
    """ Double-entry transaction model for use in Views to record activities for use with AIS """
    # Note: Currently, the Transaction model and other Librewary models are de-coupled.
    # e.g. You must do BOTH actions:
    #
    #       Patrick pays $10 deposit:
    #           contributor = Brewer.objects.get(username='patrick')
    #           contributor.contributed_cash += 10
    #           contributor.save()
    #
    #           deposit = Transaction('Asset-Cash','Equity-Deposits',10.00,[date],[staffer],[description])
    #           deposit.save()
    #
    # i.e. You have to journalize every transaction separately from affecting Brewer/Loan objects

    # This is the machine-readable chart of accounts whose values will be written to DB
    # Various Views do not need to use the string; they can use Transaction.ASSET_CASH_BOX to reference
    # the account. Further, templates will output the fancy human-intelligble string from settings.py
    # MAX STRING LENGTH = 6 -- try to limit to acronyms
    ASSET_CASH_BOX = 'ACB'
    ASSET_UNDEPOSITED_CHECKS = 'AUC'
    ASSET_CHECKING_ACCOUNT = 'ACC'
    ASSET_EQUIPMENT = 'AE'
    REVENUE_LATE_FEES = 'RLF'
    REVENUE_CONTRA_LATE_FEES_WRITE_OFF = 'RCLFWO'
    REVENUE_REGISTRATION_FEE = 'RRF'
    EXPENSE_EQUIPMENT_WRITE_OFF = 'EWO'
    EQUITY_CONTRIBUTED_CASH_DEPOSITS = 'ECCD'
    EQUITY_CONTRIBUTED_EQUIPMENT_DEPOSITS = 'ECED'
    EQUITY_LIBREWARY_NET_INCOME = 'ELNI'
    EQUITY_LIBREWARY_RETAINED_EARNINGS = 'ELRE'
    # The human-intelligble account names are defined in the site settings.py file
    librewary_chart_of_accounts = (
        (ASSET_CASH_BOX, settings.ASSET_CASH_BOX),
        (ASSET_UNDEPOSITED_CHECKS, settings.ASSET_UNDEPOSITED_CHECKS),
        (ASSET_CHECKING_ACCOUNT, settings.ASSET_CHECKING_ACCOUNT),
        (ASSET_EQUIPMENT, settings.ASSET_EQUIPMENT),
        (REVENUE_LATE_FEES, settings.REVENUE_LATE_FEES),
        (REVENUE_CONTRA_LATE_FEES_WRITE_OFF, settings.REVENUE_CONTRA_LATE_FEES_WRITE_OFF),
        (REVENUE_REGISTRATION_FEE, settings.REVENUE_REGISTRATION_FEE),
        (EXPENSE_EQUIPMENT_WRITE_OFF, settings.EXPENSE_EQUIPMENT_WRITE_OFF),
        (EQUITY_CONTRIBUTED_CASH_DEPOSITS, settings.EQUITY_CONTRIBUTED_CASH_DEPOSITS),
        (EQUITY_LIBREWARY_NET_INCOME, settings.EQUITY_LIBREWARY_NET_INCOME),
        (EQUITY_LIBREWARY_RETAINED_EARNINGS, settings.EQUITY_LIBREWARY_RETAINED_EARNINGS),
        )

    ### attributes
    # debit         account id
    # credit        account id
    # amount        amount of transaction $
    # date          date of transaction
    # staffer       authenticated user committing transaction
    # description   programmatically defined description of transaction (username/pk and activity)
    debit = models.CharField(null=False, blank=False, max_length=6, choices=librewary_chart_of_accounts)
    credit = models.CharField(null=False, blank=False, max_length=6, choices=librewary_chart_of_accounts)
    amount = models.FloatField(null=False, blank=False)
    staffer = models.ForeignKey('core.Brewer', null=False, editable=False)  # Editable is False as its programmatically entered
    description = models.TextField(null=False, blank=False)