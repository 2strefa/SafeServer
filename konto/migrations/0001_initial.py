# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RejestracjaKlienta'
        db.create_table('Rejestracja_Klienta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('jestem', self.gf('django.db.models.fields.IntegerField')()),
            ('imie', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('nazwisko', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('adres', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('miasto', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('kod_pocztowy', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('kraj', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('wojewodztwo', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('telefon', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('telefon_dodatkowy', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('nazwa_firmy', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('nip', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('regon', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('faktura_vat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('regulamin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('konto', ['RejestracjaKlienta'])

        # Adding model 'RegistrationProfile'
        db.create_table('konto_registrationprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user', unique=True, to=orm['auth.User'])),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('konto', ['RegistrationProfile'])

        # Adding model 'Zamowienia'
        db.create_table('Zamowienia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('imie', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('nazwisko', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('nazwa_serwera', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('numer_zamowienia', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('data_zamowienia', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('data_waznosci', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('rodzaj_platnosci', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('suma_netto', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=7, decimal_places=2)),
            ('suma_brutto', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=7, decimal_places=2)),
            ('realizacja', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('link_do_cpanelu', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 14, 0, 0))),
        ))
        db.send_create_signal('konto', ['Zamowienia'])

        # Adding M2M table for field dodatki on 'Zamowienia'
        m2m_table_name = db.shorten_name('Zamowienia_dodatki')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('zamowienia', models.ForeignKey(orm['konto.zamowienia'], null=False)),
            ('dodatki_id', models.ForeignKey(orm['oferta.dodatki_id'], null=False))
        ))
        db.create_unique(m2m_table_name, ['zamowienia_id', 'dodatki_id_id'])

        # Adding model 'KontaBankowe'
        db.create_table('konto_kontabankowe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazwa_banku', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('numer_konta', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('konto_aktywne', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('konto', ['KontaBankowe'])


    def backwards(self, orm):
        # Deleting model 'RejestracjaKlienta'
        db.delete_table('Rejestracja_Klienta')

        # Deleting model 'RegistrationProfile'
        db.delete_table('konto_registrationprofile')

        # Deleting model 'Zamowienia'
        db.delete_table('Zamowienia')

        # Removing M2M table for field dodatki on 'Zamowienia'
        db.delete_table(db.shorten_name('Zamowienia_dodatki'))

        # Deleting model 'KontaBankowe'
        db.delete_table('konto_kontabankowe')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'konto.kontabankowe': {
            'Meta': {'object_name': 'KontaBankowe'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'konto_aktywne': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nazwa_banku': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numer_konta': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'konto.registrationprofile': {
            'Meta': {'object_name': 'RegistrationProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'konto.rejestracjaklienta': {
            'Meta': {'object_name': 'RejestracjaKlienta', 'db_table': "'Rejestracja_Klienta'"},
            'adres': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'faktura_vat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imie': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'jestem': ('django.db.models.fields.IntegerField', [], {}),
            'kod_pocztowy': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'kraj': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'miasto': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nazwa_firmy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nazwisko': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regon': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regulamin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'telefon': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telefon_dodatkowy': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'wojewodztwo': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'konto.zamowienia': {
            'Meta': {'object_name': 'Zamowienia', 'db_table': "'Zamowienia'"},
            'cart_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'data_waznosci': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'data_zamowienia': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 14, 0, 0)'}),
            'dodatki': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oferta.Dodatki_Id']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imie': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'link_do_cpanelu': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nazwa_serwera': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nazwisko': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numer_zamowienia': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'realizacja': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rodzaj_platnosci': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'suma_brutto': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '7', 'decimal_places': '2'}),
            'suma_netto': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '7', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oferta.dodatki': {
            'Meta': {'object_name': 'Dodatki', 'db_table': "'Dodatki'"},
            'cena_netto': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'oferta_nazwa': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oferta.Oferta']", 'symmetrical': 'False'}),
            'opis': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'oferta.dodatki_id': {
            'Meta': {'object_name': 'Dodatki_Id', 'db_table': "'Dodatki_Id'"},
            'cart_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'czas_dodatki': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 14, 0, 0)'}),
            'dodatki_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oferta.Dodatki']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oferta_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'oferta.oferta': {
            'Meta': {'object_name': 'Oferta', 'db_table': "'Oferta'"},
            'antyspam_antywirus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'autoresponder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'baza_danych': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'biblioteka': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'c_code': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'c_plus_plus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cena_netto': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'codzienna_kopia_bezpieczenstwa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cron': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'django': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dostep_imap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dostep_pop_imap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dostep_www': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dziennik_serwera': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'formmail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ftp': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gestbook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'konta_pocztowe': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'konta_pocztowe_w_domenie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kreator_www': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'licznik': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod_rewire': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'multipoczta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'panel_cpanel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'perl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'php': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'poczta_mobilna': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pojemnosc': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'przekierowanie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'python': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quickinstall': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'redirected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ruby_on_rails': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'search': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ssh': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ssi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ssl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'statystyki': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subdomeny': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'transfer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'xml': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zabezpieczenie_strony_haslem': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['konto']