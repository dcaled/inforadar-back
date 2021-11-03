import pandas as pd
import tldextract

from inforadar.config import db, ma


def remove_slash(website):
    if website.endswith("/"):
        return website[:-1]
    return website


def normalize_website(website):
    website = website.replace("https://", "")
    website = website.replace("http://", "")
    website = website.replace("www.", "")
    website = website.replace("www.", "")

    ignore_list = [
        ".jornaleconomico.sapo.pt/madeira",
        ".saldopositivo.cgd.pt",
        "activadigital.activa.pt",
        "aideia.no.sapto.pt",
        "alentejo.sulinformacao.pt",
        "anea-sede.rcts.pt",
        "app.vc/revista_photok_madeira",
        "aprender.esep.pt",
        "aprh.pt/rh",
        "apsei.org.pt/proteger",
        "audio.online.pt",
        "autoclube.acp.pt",
        "brancadeneve.pt/revista-lusitana",
        "capp.iscsp.ulisboa.pt/publicacoes/cienciase",
        "centroportugal.news.pt",
        "chalgarve.min-saude.pt/lifesaving",
        "ciberevora.pt/palavra",
        "cip.org.pt/assuntos-economicos",
        "cncascais.com/hippocampus",
        "concorrencia.pt/vpt/estudos_e_publicacoes/revista_cr/paginas/revista-cr.aspx",
        "cta.ipt.pt",
        "daily.meucapital.pt",
        "diocese.braga.pt/sameiro",
        "ecos.cacia.pt",
        "eduser.ipb.pt",
        "em construção",
        "ese.ips.pt",
        "estsp.ipp.pt",
        "exaequo.apem-estudos.org",
        "exame.digital.exame.pt",
        "fc.ul.pt/newsletterdeciencias",
        "flp.fatima.pt",
        "fttp://etnografia.revues.org"
        "healthnews,pt"
        "hsb-setubal.min-saude.pt",
        "htt:/observatoriopolitico.pt/revista/apresenta",
        "http:/hdl.handle.net/10400.26/31532",
        "ics.ul.pt",
        "idi.mne.pt/pt/revistne.html",
        "ipg.pt/revistaipg",
        "jornal.amormais.pt",
        "jornalcmurtosa",
        "journals.openedition.org/laboreal",
        "journals.ual.pt/galileu",
        "jpn.up.pt",
        "lojadacultura.scml.pt",
        "madeira.gov.pt/dre",
        "medicina.ulisboa.pt/newsfmul",
        "montijo.oncity.pt",
        "noticiasde.barroselas.net",
        "oficina.turbo.pt",
        "oitavacolina.escs.ipl.pt",
        "ojornaldalixa.comunidades.net",
        "olharesdelisboa/oeiras.pt",
        "omnia.grei.pt",
        "portalahk.ccila-portugal.com",
        "psd.pt/pt/povo-livre",
        "quadrante.apm.pt",
        "queirosiana.pt;confrariaqueirosiana.blogspot.p",
        "rccs.revues.org",
        "rede.leiria-fatima.pt",
        "revista.appsicologia.org",
        "revista.arp.org.pt",
        "revistas.lis.ulusiada.pt/index.php/polis",
        "revistas.ulusofona.pt/index.php/rfdulp",
        "revistaseug.ugr.es/index.php/dedica",
        "rosario.pt.vu",
        "rpee.lnec.pt",
        "saudeinfantil.asic.pt",
        "ship.pt/sociedade-historica/boletim-informativo",
        "spea.pt/pt/publicacoes/pardela",
        "twitter.com/lordelojornal",
        "virtualazores.net/diario",
        "webs.ie.uminho.pt/ejcs",
        "wkarger.com/journal/home/275178",
        "wook.pt/wookacontece",
        "zap.aeiou.pt",
    ]

    if "@" in website:
        return website
    elif website.startswith("issuu.com/"):
        return website
    elif website.startswith("deco.proteste.pt"):
        return "deco.proteste.pt"
    elif website.endswith(".webnode.pt"):
        return website
    elif website.endswith(".blogspot.pt"):
        return website
    elif website.endswith(".wordpress.com"):
        return website
    elif website.endswith(".sapo.pt"):
        return website
    elif website.endswith(".weebly.com"):
        return website
    elif website.endswith(".iol.pt"):
        return website
    elif website.endswith(".meo.pt"):
        return website
    elif website.endswith(".uminho.pt"):
        return website
    elif website.endswith(".nit.pt"):
        return website
    elif website.endswith(".dn.pt"):
        return website
    elif website.endswith(".web.pt"):
        return website
    elif website.endswith(".blogspot.com"):
        return website
    elif ".uc.pt" in website:
        return website
    elif ".ucp.pt" in website:
        return website
    elif ".rcaap.pt" in website:
        return website
    elif "recortes.pt/" in website:
        return website
    elif "salesianos.pt" in website:
        return website
    elif "visao.sapo.pt" in website:
        return "visao.sapo.pt"
    elif ".wixsite.com" in website:
        return website
    elif website == "casa.sapo.pt/news":
        return "casa.sapo.pt"
    elif website == "eco.sapo.pt/fundos-europeus":
        return "eco.sapo.pt"
    elif website == "estrelaseouricos.sapo.pt/home":
        return "estrelaseouricos.sapo.pt"
    elif website == "ler.letras.up.pt/site/default.aspx?qry=id05":
        return "ler.letras.up.pt"
    elif website == "mediacoes.ese.ips.pt/index.php/mediacoesonline":
        return "mediacoes.ese.ips.pt"
    elif website == "observare.ual.pt/janus.net/pt":
        return "observare.ual.pt/janus.net"
    elif website == "pensarenfermagem.esel.pt/index.asp":
        return "pensarenfermagem.esel.pt"
    elif website == "publicacoes.ispa.pt/index.php/index/index":
        return "publicacoes.ispa.pt"
    elif website == "rpics.ismt.pt/index.php/ismt/index":
        return "rpics.ismt.pt"
    elif website == "visaodigital.visao.pt;visaodigital.trustinnews.pt":
        return "visaodigital.visao.pt"
    elif website == "web.estesl.ipl.pt/ojs/index.php/st/index":
        return "web.estesl.ipl.pt/ojs"
    elif website in ignore_list:
        return website

    ext = tldextract.extract(website)
    domain = "{}.{}".format(ext.domain, ext.suffix)
    # if domain != website and domain != "ecclesia.pt":
    #     print(website, domain)
    return domain


def main():
    erc_file = "ERC_registered_publishers_2021_09_06.xlsx"

    column_names = ["district", "registration_number", "registration_date", "title", "periodicity", "director", "owner",
                    "office_address", "location", "postal_code", "municipality", "support", "institutional_email",
                    "website", "content_type", "geographic_scope", "editor"]

    erc_list = pd.read_excel(erc_file, skiprows=4, usecols="A,B,E:R,W",
                             na_values=['NA'], header=None, names=column_names)
    erc_list.district = pd.Series(erc_list.district).fillna(method='ffill')
    erc_list.registration_number = erc_list.registration_number.astype('Int64')
    erc_list.registration_date = pd.to_datetime(erc_list.registration_date, dayfirst=True)

    erc_list["last_update"] = "06/09/2021"
    erc_list.last_update = pd.to_datetime(erc_list.last_update, dayfirst=True)

    erc_list.website = erc_list.website.str.lower()
    erc_list.website = erc_list.website.apply(lambda x: remove_slash(x) if pd.notnull(x) else x)
    erc_list["domain"] = erc_list.website.apply(lambda x: normalize_website(x) if pd.notnull(x) else x)
    erc_list.insert(0, 'id', range(1, 1 + len(erc_list)))

    columns_order = ["id", "registration_number", "registration_date",
                     "title", "periodicity", "support", "content_type", "geographic_scope",
                     "director", "owner", "editor",
                     "district", "municipality", "office_address", "location", "postal_code",
                     "institutional_email", "website", "domain",
                     "last_update"]

    erc_list = erc_list[columns_order]

    erc_list.to_sql(name='erc_sources', con=db.engine, index=False, if_exists='replace')

    with db.engine.connect() as con:
        con.execute('ALTER TABLE erc_sources ADD PRIMARY KEY (id);')

    # print(erc_list[erc_list["website"].isnull()])
    # print(erc_list[erc_list["registration_number"].isnull()])
    # print(erc_list.sort_values(by=['registration_number']))

    # print(erc_list["website"])
    # print(erc_list)


if __name__ == '__main__':
    main()
