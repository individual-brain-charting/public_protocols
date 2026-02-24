<?xml version="1.0" encoding="iso-8859-1"?>



<xsl:stylesheet version="1.0"

  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"

  xmlns:dt="urn:schemas-microsoft-com:datatypes">

	<xsl:template match="/">

		<html>

			<head>

				<title>Experiment Advisor Report</title>



				<style type="text/css">

          body { font-family:Arial; }

          th { background-color:#1E1D72; color:white; }

          td { border-style:solid; border-width:1pt; border-color:#1E1D72; }

          table { width:60%;  border-color:#1E1D72; border-style:solid; border-width:1pt; border-collapse:collapse; }

          .trOdd { background-color:#F0F8FF; }

          .trEven { background-color:#F5F5F5; }



				</style>

			</head>

			<body>



				<h1>Experiment Advisor Report</h1>



				<img src = "data:image/jpeg;base64,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" />



				<!-- ExperimentInfo -->

				<h2>Experiment Info</h2>



				<table>



					<xsl:for-each select="Report/ExperimentInfo">



						<tr>



							<td>ExperimentName:</td>



							<td>



								<xsl:value-of select="ExperimentName"/>



							</td>



						</tr>







						<tr>



							<td>Session Date/Time:</td>



							<td>



								<xsl:value-of select="SessionDate"/>

                <xsl:text disable-output-escaping="yes">&amp;</xsl:text>nbsp;

                <xsl:value-of select="SessionTime"/>



							</td>



						</tr>







						<tr>



							<td>Subject</td>



							<td>



								<xsl:value-of select="Subject"/>



							</td>



						</tr>







						<tr>



							<td>Session</td>



							<td>



								<xsl:value-of select="Session"/>



							</td>



						</tr>







						<tr>



							<td>Group</td>



							<td>



								<xsl:value-of select="Group"/>



							</td>



						</tr>



						<tr>



							<td>Elapsed Time</td>



							<td>



								<xsl:value-of select="ElapsedTime"/>



							</td>



						</tr>          







					</xsl:for-each>



				</table>







				<!-- TimeAuditInfo -->







				<h2>Onset To Onset Stats</h2>

				<xsl:variable name="resultCount" select="count(Report/TimeAuditInfo/TimeAuditObjects/TimeAuditObject/OnsetToOnsetStats/OnsetToOnsetStat)" />



				<xsl:choose>



					<xsl:when test="$resultCount = 0">

						<blockquote>(none)</blockquote>

					</xsl:when>



					<xsl:otherwise>



						<table>







							<tr>



								<th>Object</th>



								<th>Expected</th>



								<th>N</th>



								<th>Mean</th>



								<th>StdDev</th>



								<th>Min</th>



								<th>Max</th>             



							</tr>







							<xsl:for-each select="Report/TimeAuditInfo/TimeAuditObjects/TimeAuditObject/OnsetToOnsetStats/OnsetToOnsetStat">





								<xsl:variable name="css-class">

									<xsl:choose>

										<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

										<xsl:otherwise>trOdd</xsl:otherwise>

									</xsl:choose>

								</xsl:variable>





								<tr class="{$css-class}">



									<td>





										<xsl:value-of select="Name"/>



									</td>



									<td>



										<xsl:value-of select="Expected"/>



									</td>



									<td>



										<xsl:value-of select="N"/>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="Mean/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(Mean, "0")'/>

											</xsl:when>

											<xsl:when test="Mean/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="Mean = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="Mean"/>

											</xsl:otherwise>

										</xsl:choose>





									</td>



									<td>



										<xsl:choose>

											<xsl:when test="StdDevP/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(StdDevP, "0")'/>

											</xsl:when>

											<xsl:when test="StdDevP/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="StdDevP = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="StdDevP"/>

											</xsl:otherwise>

										</xsl:choose>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="Min/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(Min, "0")'/>

											</xsl:when>

											<xsl:when test="Min/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="Min = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="Min"/>

											</xsl:otherwise>

										</xsl:choose>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="Max/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(Max, "0")'/>

											</xsl:when>

											<xsl:when test="Max/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="Max = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="Max"/>

											</xsl:otherwise>

										</xsl:choose>





									</td>                  



								</tr>











							</xsl:for-each>



						</table>



					</xsl:otherwise>



				</xsl:choose>



				<h2>Onset Delay Stats</h2>



				<xsl:variable name="OnsetDelayCount" select="count(Report/TimeAuditInfo/TimeAuditObjects/TimeAuditObject/OnsetDelayStats)" />



				<xsl:choose>



					<xsl:when test="$OnsetDelayCount = 0">

						<blockquote>(none)</blockquote>

					</xsl:when>



					<xsl:otherwise>





						<table>



							<tr>



								<th>Object</th>



								<th>N</th>



								<th>Mean</th>



								<th>StdDev</th>



								<th>Min</th>



								<th>Max</th>



							</tr>







							<xsl:for-each select="Report/TimeAuditInfo/TimeAuditObjects/TimeAuditObject/OnsetDelayStats">







								<xsl:variable name="css-class">

									<xsl:choose>

										<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

										<xsl:otherwise>trOdd</xsl:otherwise>

									</xsl:choose>

								</xsl:variable>





								<tr class="{$css-class}">



									<td>



										<xsl:value-of select="Name"/>



									</td>



									<td>



										<xsl:value-of select="N"/>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="Mean/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(Mean, "0")'/>

											</xsl:when>

											<xsl:when test="Mean/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="Mean = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="Mean"/>

											</xsl:otherwise>

										</xsl:choose>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="StdDevP/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(StdDevP, "0")'/>

											</xsl:when>

											<xsl:when test="StdDevP/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="StdDevP = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="StdDevP"/>

											</xsl:otherwise>

										</xsl:choose>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="Min/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(Min, "0")'/>

											</xsl:when>

											<xsl:when test="Min/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="Min = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="Min"/>

											</xsl:otherwise>

										</xsl:choose>





									</td>



									<td>



										<xsl:choose>

											<xsl:when test="Max/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(Max, "0")'/>

											</xsl:when>

											<xsl:when test="Max/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="Max = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="Max"/>

											</xsl:otherwise>

										</xsl:choose>





									</td>







								</tr>



							</xsl:for-each>



						</table>



					</xsl:otherwise>

				</xsl:choose>



				<h2>Load Time Stats</h2>



				<xsl:variable name="LoadTimeCount" select="count(Report/TimeAuditInfo/TimeAuditObjects/TimeAuditObject/LoadTimeStats)" />



				<xsl:choose>



					<xsl:when test="$LoadTimeCount= 0">

						<blockquote>(none)</blockquote>

					</xsl:when>



					<xsl:otherwise>



						<table>

							<tr>



								<th>Object</th>



								<th>N</th>



								<th>Mean</th>



								<th>StdDev</th>



								<th>Min</th>



								<th>Max</th>



							</tr>







							<xsl:for-each select="Report/TimeAuditInfo/TimeAuditObjects/TimeAuditObject/LoadTimeStats">







								<xsl:variable name="css-class">

									<xsl:choose>

										<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

										<xsl:otherwise>trOdd</xsl:otherwise>

									</xsl:choose>

								</xsl:variable>





								<tr class="{$css-class}">



									<td>



										<xsl:value-of select="Name"/>



									</td>



									<td>



										<xsl:value-of select="N"/>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="Mean/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(Mean, "0")'/>

											</xsl:when>

											<xsl:when test="Mean/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="Mean = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="Mean"/>

											</xsl:otherwise>

										</xsl:choose>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="StdDevP/@dt:dt = 'r8'">

												<xsl:value-of select='format-number(StdDevP, "0")'/>

											</xsl:when>

											<xsl:when test="StdDevP/@dt:dt = 'boolean'">

												<xsl:choose>

													<xsl:when test="StdDevP = 1">Yes</xsl:when>

													<xsl:otherwise>No</xsl:otherwise>

												</xsl:choose>

											</xsl:when>

											<xsl:otherwise>

												<xsl:value-of select="StdDevP"/>

											</xsl:otherwise>

										</xsl:choose>



									</td>



									<td>



										<xsl:choose>

											<xsl:when test="N = 0">

						0

											</xsl:when>

											<xsl:otherwise>



												<xsl:choose>

													<xsl:when test="Min/@dt:dt = 'r8'">

														<xsl:value-of select='format-number(Min, "0")'/>

													</xsl:when>

													<xsl:when test="Min/@dt:dt = 'boolean'">

														<xsl:choose>

															<xsl:when test="Min = 1">Yes</xsl:when>

															<xsl:otherwise>No</xsl:otherwise>

														</xsl:choose>

													</xsl:when>

													<xsl:otherwise>

														<xsl:value-of select="Min"/>

													</xsl:otherwise>

												</xsl:choose>

											</xsl:otherwise>

										</xsl:choose>







									</td>



									<td>



										<xsl:choose>

											<xsl:when test="N = 0">

						0

											</xsl:when>

											<xsl:otherwise>

												<xsl:choose>

													<xsl:when test="Max/@dt:dt = 'r8'">

														<xsl:value-of select='format-number(Max, "0")'/>

													</xsl:when>

													<xsl:when test="Max/@dt:dt = 'boolean'">

														<xsl:choose>

															<xsl:when test="Max = 1">Yes</xsl:when>

															<xsl:otherwise>No</xsl:otherwise>

														</xsl:choose>

													</xsl:when>

													<xsl:otherwise>

														<xsl:value-of select="Max"/>

													</xsl:otherwise>

												</xsl:choose>

											</xsl:otherwise>

										</xsl:choose>







									</td>







								</tr>

							</xsl:for-each>

						</table>

					</xsl:otherwise>

				</xsl:choose>



				<!-- MovieInfo -->





				<!-- AdvisorModuleFindings -->



				<h2>Experiment Advisor Findings</h2>



				<xsl:variable name="ExperimentAdvisorModuleFindingCount" select="count(Report/AdvisorModuleFindings/AdvisorModuleFinding)" />



				<xsl:choose>



					<xsl:when test="$ExperimentAdvisorModuleFindingCount = 0">

						<blockquote>(none)</blockquote>

					</xsl:when>



					<xsl:otherwise>





						<table>







							<tr>



								<th>Caption</th>



								<th>Category</th>



								<th>Message</th>



								<th>Occurrences</th>



							</tr>







							<xsl:for-each select="Report/AdvisorModuleFindings/AdvisorModuleFinding">





								<xsl:variable name="css-class">

									<xsl:choose>

										<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

										<xsl:otherwise>trOdd</xsl:otherwise>

									</xsl:choose>

								</xsl:variable>





								<tr class="{$css-class}">



									<td>



										<xsl:value-of select="AdvisorModuleCaption"/>



										<xsl:variable name="urlParameters">GUID=<xsl:value-of select="AdvisorModuleDefinitionGuid"/>&amp;Message=<xsl:value-of select="MessageUrlEscape"/>

										</xsl:variable>



										<xsl:text disable-output-escaping="yes">

											<![CDATA[&nbsp;&nbsp;<a href="http://www.pstnet.com/support/advisor/Help.aspx?]]>

										</xsl:text>

										<xsl:value-of select="$urlParameters"/>

										<xsl:text disable-output-escaping="yes">

											<![CDATA["><img alt="" style="border: 0;" src="data:image/png;base64,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" /></a>]]></xsl:text>





									</td>



									<td>



										<xsl:value-of select="Category"/>



									</td>



									<td>



										<xsl:value-of select="Message"/>



									</td>



									<td>



										<xsl:value-of select="MessageCount"/>



									</td>



								</tr>

							</xsl:for-each>



						</table>

					</xsl:otherwise>

				</xsl:choose>



				<!-- AdvisorModuleInfo -->



				<h2>Experiment Advisor Modules</h2>



				<xsl:variable name="ExperimentAdvisorModuleCount" select="count(Report/AdvisorModules/AdvisorModule)" />



				<xsl:choose>



					<xsl:when test="$ExperimentAdvisorModuleCount= 0">

						<blockquote>(none)</blockquote>

					</xsl:when>



					<xsl:otherwise>



						<table>

							<tr>

								<th>Caption</th>



								<th>Enabled</th>



								<th>Description</th>

							</tr>



							<xsl:for-each select="Report/AdvisorModules/AdvisorModule">



								<xsl:variable name="css-class">

									<xsl:choose>

										<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

										<xsl:otherwise>trOdd</xsl:otherwise>

									</xsl:choose>

								</xsl:variable>





								<tr class="{$css-class}">





									<td>

										<xsl:value-of select="Caption"/>

										<xsl:text disable-output-escaping="yes">

											<![CDATA[&nbsp;&nbsp;<a href="http://www.pstnet.com/support/advisor/Help.aspx?GUID=]]>

										</xsl:text>

										<xsl:value-of select="DefinitionGuid"/>

										<xsl:text disable-output-escaping="yes">

											<![CDATA["><img alt="" style="border: 0;" src="data:image/png;base64,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" /></a>]]></xsl:text>

									</td>



									<td>

										<xsl:choose>

											<xsl:when test="Enabled = 1">Yes</xsl:when>

											<xsl:otherwise>No</xsl:otherwise>

										</xsl:choose>

									</td>



									<td>

										<xsl:value-of select="Description"/>

									</td>



								</tr>

							</xsl:for-each>



						</table>



					</xsl:otherwise>

				</xsl:choose>



				<!-- ClockInfo -->



				<h2>Clock Info</h2>



				<table>



					<xsl:for-each select="Report/Clock/Property">



						<xsl:variable name="css-class">

							<xsl:choose>

								<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

								<xsl:otherwise>trOdd</xsl:otherwise>

							</xsl:choose>

						</xsl:variable>





						<tr class="{$css-class}">



							<td>



								<xsl:value-of select="PropertyName"/>



							</td>



							<td>



								<xsl:choose>

									<xsl:when test="PropertyValue/@dt:dt = 'r8'">

										<xsl:value-of select='format-number(PropertyValue, "0")'/>

									</xsl:when>

									<xsl:when test="PropertyValue/@dt:dt = 'boolean'">

										<xsl:choose>

											<xsl:when test="PropertyValue = 1">Yes</xsl:when>

											<xsl:otherwise>No</xsl:otherwise>

										</xsl:choose>

									</xsl:when>

									<xsl:otherwise>

										<xsl:value-of select="PropertyValue"/>

									</xsl:otherwise>

								</xsl:choose>





							</td>



						</tr>



					</xsl:for-each>



				</table>



				<!-- DeviceInfo -->



				<h2>Device Info</h2>



				<xsl:for-each select="Report/Devices/Device">

					<table>





						<xsl:for-each select="Property">



							<xsl:variable name="css-class">

								<xsl:choose>

									<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

									<xsl:otherwise>trOdd</xsl:otherwise>

								</xsl:choose>

							</xsl:variable>



							<tr class="{$css-class}">



								<td width="25%">



									<xsl:value-of select="PropertyName"/>



								</td>



								<td>



									<xsl:choose>

										<xsl:when test="PropertyValue/@dt:dt = 'r8'">

											<xsl:value-of select='format-number(PropertyValue, "0.##")'/>

										</xsl:when>

										<xsl:when test="PropertyValue/@dt:dt = 'boolean'">

											<xsl:choose>

												<xsl:when test="PropertyValue = 1">Yes</xsl:when>

												<xsl:otherwise>No</xsl:otherwise>

											</xsl:choose>

										</xsl:when>

										<xsl:otherwise>

											<xsl:value-of select="PropertyValue"/>

										</xsl:otherwise>

									</xsl:choose>



								</td>



							</tr>







						</xsl:for-each>



					</table>



					<br />



				</xsl:for-each>



				<!-- Running Applications -->

				<h2>Running Applications</h2>

				<table>

					<tr>

						<th>Image Name</th>

						<th>Process ID</th>

						<th>Working Set Size (KB)</th>

						<th>Full Name</th>

						<th>Version</th>

						<th>Last Modified</th>

						<th>Size</th>

					</tr>

					

					<xsl:for-each select="Report/RunningApplications/RunningApplication">

						<xsl:variable name="css-class">

							<xsl:choose>

								<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

								<xsl:otherwise>trOdd</xsl:otherwise>

							</xsl:choose>

						</xsl:variable>

						<tr class="{$css-class}">

							<td>

								<xsl:value-of select="ImageName"/>

							</td>

							<td>

								<xsl:value-of select="ProcessID"/>

							</td>

							<td>

								<xsl:value-of select="WorkingSetSizeKB"/>

							</td>

							<td>

								<xsl:value-of select="ImageFullName"/>

							</td>		

							<td>

								<xsl:value-of select="FileVersion"/>

							</td>	

							<td>

								<xsl:value-of select="LastModifiedDateTime"/>

							</td>								

							<td>

								<xsl:value-of select="ImageSize"/>

							</td>

						</tr>

					</xsl:for-each>

				</table>
				
				<!-- OperatingSystemInfo -->
				
				<br />
				<h2>Operating System Info</h2>
				
				
					<table>


						<xsl:for-each select="Report/OperatingSystem/Property">



							<xsl:variable name="css-class">

								<xsl:choose>

									<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

									<xsl:otherwise>trOdd</xsl:otherwise>

								</xsl:choose>

							</xsl:variable>



							<tr class="{$css-class}">



								<td width="25%">



									<xsl:value-of select="PropertyName"/>



								</td>



								<td>



									<xsl:choose>

										<xsl:when test="PropertyValue/@dt:dt = 'r8'">

											<xsl:value-of select='format-number(PropertyValue, "0.##")'/>

										</xsl:when>

										<xsl:when test="PropertyValue/@dt:dt = 'boolean'">

											<xsl:choose>

												<xsl:when test="PropertyValue = 1">Yes</xsl:when>

												<xsl:otherwise>No</xsl:otherwise>

											</xsl:choose>

										</xsl:when>

										<xsl:otherwise>

											<xsl:value-of select="PropertyValue"/>

										</xsl:otherwise>

									</xsl:choose>



								</td>



							</tr>

						</xsl:for-each>

					</table>
					
				<br />
					
				<br />
				
				<h2>BIOS Info</h2>
				
				
					<table>


						<xsl:for-each select="Report/BIOS/Type0/Property">



							<xsl:variable name="css-class">

								<xsl:choose>

									<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

									<xsl:otherwise>trOdd</xsl:otherwise>

								</xsl:choose>

							</xsl:variable>



							<tr class="{$css-class}">



								<td width="25%">



									<xsl:value-of select="PropertyName"/>



								</td>



								<td>



									<xsl:choose>

										<xsl:when test="PropertyValue/@dt:dt = 'r8'">

											<xsl:value-of select='format-number(PropertyValue, "0.##")'/>

										</xsl:when>

										<xsl:when test="PropertyValue/@dt:dt = 'boolean'">

											<xsl:choose>

												<xsl:when test="PropertyValue = 1">Yes</xsl:when>

												<xsl:otherwise>No</xsl:otherwise>

											</xsl:choose>

										</xsl:when>

										<xsl:otherwise>

											<xsl:value-of select="PropertyValue"/>

										</xsl:otherwise>

									</xsl:choose>



								</td>



							</tr>

						</xsl:for-each>

					</table>
					
					<br />
					
					<table>


						<xsl:for-each select="Report/BIOS/Type1/Property">



							<xsl:variable name="css-class">

								<xsl:choose>

									<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

									<xsl:otherwise>trOdd</xsl:otherwise>

								</xsl:choose>

							</xsl:variable>



							<tr class="{$css-class}">



								<td width="25%">



									<xsl:value-of select="PropertyName"/>



								</td>



								<td>



									<xsl:choose>

										<xsl:when test="PropertyValue/@dt:dt = 'r8'">

											<xsl:value-of select='format-number(PropertyValue, "0.##")'/>

										</xsl:when>

										<xsl:when test="PropertyValue/@dt:dt = 'boolean'">

											<xsl:choose>

												<xsl:when test="PropertyValue = 1">Yes</xsl:when>

												<xsl:otherwise>No</xsl:otherwise>

											</xsl:choose>

										</xsl:when>

										<xsl:otherwise>

											<xsl:value-of select="PropertyValue"/>

										</xsl:otherwise>

									</xsl:choose>



								</td>



							</tr>

						</xsl:for-each>

					</table>
					
					<br />
					
					<table>


						<xsl:for-each select="Report/BIOS/Type2/Property">



							<xsl:variable name="css-class">

								<xsl:choose>

									<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

									<xsl:otherwise>trOdd</xsl:otherwise>

								</xsl:choose>

							</xsl:variable>



							<tr class="{$css-class}">



								<td width="25%">



									<xsl:value-of select="PropertyName"/>



								</td>



								<td>



									<xsl:choose>

										<xsl:when test="PropertyValue/@dt:dt = 'r8'">

											<xsl:value-of select='format-number(PropertyValue, "0.##")'/>

										</xsl:when>

										<xsl:when test="PropertyValue/@dt:dt = 'boolean'">

											<xsl:choose>

												<xsl:when test="PropertyValue = 1">Yes</xsl:when>

												<xsl:otherwise>No</xsl:otherwise>

											</xsl:choose>

										</xsl:when>

										<xsl:otherwise>

											<xsl:value-of select="PropertyValue"/>

										</xsl:otherwise>

									</xsl:choose>



								</td>



							</tr>

						</xsl:for-each>

					</table>
					
					<br />
					
					<table>


						<xsl:for-each select="Report/BIOS/Type3/Property">



							<xsl:variable name="css-class">

								<xsl:choose>

									<xsl:when test="position() mod 2 = 0">trEven</xsl:when>

									<xsl:otherwise>trOdd</xsl:otherwise>

								</xsl:choose>

							</xsl:variable>



							<tr class="{$css-class}">



								<td width="25%">



									<xsl:value-of select="PropertyName"/>



								</td>



								<td>



									<xsl:choose>

										<xsl:when test="PropertyValue/@dt:dt = 'r8'">

											<xsl:value-of select='format-number(PropertyValue, "0.##")'/>

										</xsl:when>

										<xsl:when test="PropertyValue/@dt:dt = 'boolean'">

											<xsl:choose>

												<xsl:when test="PropertyValue = 1">Yes</xsl:when>

												<xsl:otherwise>No</xsl:otherwise>

											</xsl:choose>

										</xsl:when>

										<xsl:otherwise>

											<xsl:value-of select="PropertyValue"/>

										</xsl:otherwise>

									</xsl:choose>



								</td>



							</tr>

						</xsl:for-each>

					</table>
					
					<br />
					<br />
					<br />

			</body>



		</html>



	</xsl:template>



</xsl:stylesheet>







