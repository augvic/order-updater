from win32com.client import GetObject

class SapClient:
    
    def init(self) -> None:
        try:
            gui = GetObject("SAPGUI")
            app = gui.GetScriptingEngine
            con = app.Children(0)
        except:
            raise Exception("SAP não está aberto.")
        for id in range(0, 7):
            try:
                session = con.Children(id)
                if "SAP Easy Access" in session.ActiveWindow.Text:
                    self.session = session
                    return
                else:
                    continue
            except:
                pass
        else:
            raise Exception("Não foi encontrado janela SAP disponível para conexão.")
    
    def _open_transaction(self, transaction: str) -> None:
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/N" + transaction
        self.session.findById("wnd[0]").sendVKey(0)
        status_bar = None
        status_bar = self.session.findById("wnd[0]/sbar").text
        if "Sem autorização" in status_bar:
            raise Exception(f"Sem acesso a transação: {transaction}.")
    
    def _get_text(self, id: str) -> str:
        try:
            return self.session.findById(id).text
        except:
            raise Exception(f"ID SAP não encontrado: {id}.")
    
    def _set_text(self, id: str, text: str) -> None:
        try:
            self.session.findById(id).text = text
        except:
            raise Exception(f"ID SAP não encontrado: {id}.")
    
    def _press_enter(self, index: str) -> None:
        self.session.findById(rf"wnd[{index}]").sendVKey(0)
    
    def _press_button(self, id: str) -> None:
        try:
            self.session.findById(id).press()
        except:
            raise Exception(f"ID SAP não encontrado: {id}")
    
    def _select_tab(self, id: str) -> None:
        try:
            self.session.findById(id).select()
        except:
            raise Exception(f"ID SAP não encontrado: {id}")
    
    def _get_key(self, id: str) -> str:
        try:
            return self.session.findById(id).key
        except:
            raise Exception(f"ID SAP não encontrado: {id}")
    
    def _set_key(self, id: str, key: str) -> None:
        try:
            self.session.findById(id).key = key
        except:
            raise Exception(f"ID SAP não encontrado: {id}")
    
    def _press_back(self, index: str) -> None:
        self.session.findById(rf"wnd[{index}]/tbar[0]/btn[3]").press()
    
    def _set_partner_za(self, partner_code: str) -> None:
        for row in range(0, 20):
            key = self._get_key(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/cmbGVS_TC_DATA-REC-PARVW[0,{row}]")
            if key == "ZA":
                self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/ctxtGVS_TC_DATA-REC-PARTNER[1,{row}]", partner_code)
                break
    
    def _enter_in_order(self, order: str) -> None:
        self._open_transaction("VA02")
        self._set_text(r"wnd[0]/usr/ctxtVBAK-VBELN", order)
        self._press_enter("0")
        self._press_enter("0")
    
    def _go_to_header(self) -> None:
        self._press_button(r"wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD")
    
    def _set_partner(self, partner_code: str) -> None:
        self._select_tab(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08")
        self._set_partner_za(partner_code)
        self._press_enter("0")
    
    def _set_office(self) -> None:
        self._select_tab(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01")
        self._set_text(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4301/ctxtVBAK-VKBUR", "1148")
        self._set_text(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4301/ctxtVBAK-VKGRP", "058")
    
    def _press_go(self, index: str) -> None:
        self.session.findById(rf"wnd[{index}]").sendVKey(2)
    
    def focus(self, id: str) -> None:
        try:
            self.session.findById(id).setFocus()
        except:
            raise Exception(f"ID SAP não encontrado: {id}")
    
    def _access_item_level(self) -> None:
        self.focus(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,0]")
        self._press_go("0")
    
    def _reply_comission(self) -> None:
        self._press_button(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnBT_REPL_COMISS")
        self._press_button(r"wnd[1]/usr/btnBUTTON_1")
        self._press_button(r"wnd[1]/tbar[0]/btn[0]")
    
    def _fill_out_comission(self, comission_code: str) -> None:
        self._press_button(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD")
        self._set_key(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,0]", "Z2")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,0]", "2000006653")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,0]", "0,22")
        self._press_button(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD")
        self._set_key(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,1]", "Z3")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,1]", "5000002513")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,1]", "0,30")
        self._press_button(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD")
        self._set_key(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,2]", "Z5")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,2]", "2000005674")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,2]", "0,22")
        self._press_button(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD")
        self._set_key(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,3]", "Z6")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,3]", comission_code)
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,3]", "0,40")
        self._press_button(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD")
        self._set_key(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,4]", "Z7")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,4]", "COMPROV")
        self._set_text(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,4]", "0,30")
        self._press_enter("0")
        self._reply_comission()
    
    def _set_comission(self, comission_code: str) -> None:
        self._select_tab(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15")
        self._fill_out_comission(comission_code)
    
    def _save_order(self) -> None:
        self._press_button(r"wnd[0]/tbar[0]/btn[11]")
        try:
            self._press_button(r"wnd[0]/tbar[1]/btn[18]")
        except:
            pass
        msg_bar = self._get_text(r"wnd[0]/sbar")
        if "sem garantia" in msg_bar:
            raise Exception("Ordem sem garantia.")
        elif "Não foi efetuada" in msg_bar:
            return
        elif "foi gravado" in msg_bar:
            return
        else:
            self._press_enter("0")
            try:
                self._press_button(r"wnd[1]/usr/btnSPOP-VAROPTION1")
            except:
                pass
            return
    
    def _flag_element(self, id: str, true_false: bool) -> None:
        self.session.findById(id).selected = true_false
    
    def _find_libe_row(self) -> None:
        row = 1
        while True:
            text = self._get_text(fr"wnd[0]/usr/tabsTABSTRIP_0300/tabpANWS/ssubSUBSCREEN:SAPLBSVA:0302/tblSAPLBSVATC_EO/txtJEST_BUF_EO-ETX04[1,0]")
            if text == "LIBE":
                break
            else:
                self.session.findById(r"wnd[0]/usr/tabsTABSTRIP_0300/tabpANWS/ssubSUBSCREEN:SAPLBSVA:0302/tblSAPLBSVATC_EO").verticalScrollbar.position = row + 1
    
    def _set_libe(self) -> None:
        self._select_tab(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\11")
        self._press_button(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\11/ssubSUBSCREEN_BODY:SAPMV45A:4305/btnBT_KSTC")
        self._find_libe_row()
        self._flag_element(r"wnd[0]/usr/tabsTABSTRIP_0300/tabpANWS/ssubSUBSCREEN:SAPLBSVA:0302/tblSAPLBSVATC_EO/chkJ_STMAINT-ANWSO[0,0]", True)
    
    def go_home(self) -> None:
        try:
            while True:
                if self.session.ActiveWindow.Text == "SAP Easy Access":
                    break
                else:
                    try:
                        self.session.findById("wnd[1]").close()
                    except:
                        pass
                    try:
                        self.session.findById("wnd[0]").sendVKey(3)
                    except:
                        pass
                    try:
                        self.session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
                    except:
                        pass
        except Exception as error:
            raise Exception(f"Error in (SapClient) component in (go_home) method: {error}.")
    
    def update_order(self, order: str, partner_code: str, comission_code: str) -> None:
        try:
            self._enter_in_order(order)
            self._go_to_header()
            self._set_office()
            self._set_partner(partner_code)
            self._set_libe()
            self._press_back("0")
            self._press_back("0")
            self._access_item_level()
            self._set_comission(comission_code)
            self._save_order()
        except Exception as error:
            raise Exception(f"Error in (SapClient) component in (update_order) method: {error}.")
